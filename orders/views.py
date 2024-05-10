from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from ipware import get_client_ip

from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

# Create your views here.
# razerpay
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from .vnpay import vnpay

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# payments view
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    products = OrderProduct.objects.filter(order_id=order.id)
    # Store transaction details in transaction table
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move cart items to order items
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        # variations adding to order product
        # check variation variable name in orders cart and payment to avido confusing in future
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products from orginal stock
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # Empty the cart
    CartItem.objects.filter(user=request.user).delete()

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    # Send email to the user ( with order details )
    mail_subject = 'Thank you for your order.'
    message = render_to_string('orders/order_mail.html', {
        'user': request.user,
        'order': order,
        'items': cart_items,
        'url': 'http://127.0.0.1:8000/orders/order_complete/?' + 'order_number=' + order.order_number + '&payment_id=' + payment.payment_id,

    })

    to_email = order.email
    print(to_email)
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()

    # send order number & transcation id back to sendData method via JasonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items_ttl = CartItem.objects.filter(user=current_user, is_active=True)
    cart_count = cart_items_ttl.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_items in cart_items_ttl:
        total += (cart_items.product.price * cart_items.quantity)
        quantity += cart_items.quantity

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            data = Order()
            data.user = current_user
            data.full_name = form.cleaned_data['full_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.road = form.cleaned_data['road']
            data.ward = form.cleaned_data['ward']
            data.district = form.cleaned_data['district']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.payment_method = form.cleaned_data['payment_method']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # genarate order number and store in order table
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%d%m%Y")

            payment_type = data.payment_method

            amount = int(grand_total * 100)

            if payment_type == "VNPAY":

                order_id = form.cleaned_data['order_id']
                bank_code = form.cleaned_data['bank_code']
                language = form.cleaned_data['language']
                ipaddr = get_client_ip(request)

                vnp = vnpay()
                vnp.requestData['vnp_Version'] = '2.1.0'
                vnp.requestData['vnp_Command'] = 'pay'
                vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
                vnp.requestData['vnp_Amount'] = amount
                vnp.requestData['vnp_CurrCode'] = 'VND'
                vnp.requestData['vnp_TxnRef'] = order_id
                vnp.requestData['vnp_OrderInfo'] = form.cleaned_data['order_note']
                vnp.requestData['vnp_OrderType'] = "billpayment"

                if language and language != '':
                    vnp.requestData['vnp_Locale'] = language
                else:
                    vnp.requestData['vnp_Locale'] = 'vn'
                if bank_code and bank_code != "":
                    vnp.requestData['vnp_BankCode'] = bank_code

                vnp.requestData['vnp_CreateDate'] = timezone.now().strftime('%Y%m%d%H%M%S')
                vnp.requestData['vnp_IpAddr'] = ipaddr
                vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
                vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
                return redirect(vnpay_payment_url)
            else:
                print("Form input not validate")
            return render(request, 'orders/payments.html', context)
        else:
            return HttpResponse('Form is not valid')
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        tax = (2 * order.order_total) / 100
        subtotal = order.order_total - tax
        subtotal = round(subtotal, 2)
        grand_total = order.order_total
        tax = round(tax, 2)
        context = {
            'user_name': order.user.full_name,
            'date': order.date,
            'note': order.order_note,
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'transID': transID,
            'address': order.address,
            'subtotal': subtotal,
            'tax': tax,
            'grand_total': grand_total,
        }

        return render(request, 'orders/order_complete.html', context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('/')


@csrf_exempt
def paymenthandler(request, total=0, quantity=0):
    # Only accept POST request
    if request.method == 'POST':
        try:
            # get the required parameters from post request
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            # result = razorpay_client.utility.verify_payment_signature(params_dict)
            result = signature
            if result is not None:
                amount = request.session['razorpay_amount']
                print(amount)
                try:
                    # Capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    # Render Success Page on successfull capture of payment

                    order = Order.objects.get(user=request.user, is_ordered=False, order_number=razorpay_order_id)
                    print(order)
                    # Save payment information
                    payment = Payment(
                        user=request.user,
                        payment_id=payment_id,
                        payment_method='RazorPay',
                        amount_paid=order.order_total,
                        status='Completed',
                    )
                    payment.save()
                    print(payment)
                    order.payment = payment
                    order.is_ordered = True
                    order.save()
                    print("order dw", order)

                    # Move the cart item to order product table
                    cart_items = CartItem.objects.filter(user=request.user)

                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = request.user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.order_total = order.order_total
                        orderproduct.ordered = True
                        orderproduct.save()

                        # variations adding to order product
                        # check variation variable name in orders cart and payment to avido confusing in future
                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variations.all()
                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.variation.set(product_variation)
                        orderproduct.save()

                        # Reduce the quantity of the sold products from orginal stock
                        product = Product.objects.get(id=item.product_id)
                        product.stock -= item.quantity
                        product.save()

                    # Clear the Cart
                    CartItem.objects.filter(user=request.user).delete()
                    print("cart cleared")

                    # Send email to the user ( with order details )
                    mail_subject = 'Thank you for your order.'
                    message = render_to_string('orders/order_mail.html', {
                        'user': request.user,
                        'order': order,
                        'items': cart_items,
                        'url': 'http://127.0.0.1:8000/orders/order_complete/?' + 'order_number=' + order.order_number + '&payment_id=' + payment.payment_id,

                    })
                    to_email = order.email
                    print(to_email)
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    send_email.content_subtype = "html"
                    send_email.send()

                    # Send Transaction Successfull
                    param = (
                            "order_number=" + order.order_number + "&payment_id=" + payment.payment_id
                    )
                    print(param)
                    # Capture the payment
                    return redirect('/orders/order_complete/?' + param)


                except Exception as e:
                    # If there is an error while capturing payment
                    messages.error(request, "Payment Failed1")
                    return HttpResponse("Payment Failed")
                    return redirect("place_order")


            else:
                messages.error(request, "Payment Failed2")
                return HttpResponse("Payment Failed2")
                return redirect("place_order")

                # if signature verification fails

        except:
            messages.error(request, "Payment Failed3")
            return HttpResponse("Payment Failed3")
            return redirect("place_order")

            # If required parameters in not found in POST data

    else:
        return redirect("place_order")
        return HttpResponse("Payment Failed3")
        # if request is not POST


def add_review(request, id):
    if request.method == "POST":
        return HttpResponse('Form is not valid')