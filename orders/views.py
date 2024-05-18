from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from accounts.models import EventUser
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from forex_python.converter import CurrencyRates
from .vnpay import vnpay
from decouple import config

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_formatted_time():
    now = timezone.now()
    formatted_time = now.strftime('%Y%m%d%H%M%S')
    return formatted_time


def payments(request, order_id, payment_id):
    order = Order.objects.get(is_ordered=True, order_number=order_id)
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    mail_subject = 'Thank you for your order.'
    current_site = get_current_site(request)

    parameters = {
        'user': request.user,
        'order': order,
        'items': cart_items,
        'url': f'http://{current_site}/accounts/order_details/' + order_id,
    }
    mail_body = render_to_string('orders/order_mail.html', parameters)
    email = EmailMessage(
        subject=mail_subject,
        body=mail_body,
        from_email=config('EMAIL_HOST_USER'),
        to=[request.user.email],
    )
    email.content_subtype = "html"
    try:
        email.send()
    except Exception as e:
        messages.error(request, 'error: ' + str(e))

def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']

        amount_usd = amount/25000

        order = Order.objects.get(order_number=order_id, is_ordered=False)
        if order.is_view == False:
            return redirect('order_details', order_id=order.order_number)
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            product = Product.objects.get(id=item.product_id)
            event = EventUser.objects.filter(user_id=request.user.id, product_id=product.id, event_type='pay')
            if event:
                event.frequency += 1
                event.event_timestamp = timezone.now()
                event.save()
            else:
                user_event = EventUser(
                    user_id=request.user.id,
                    product_id=product.id,
                    event_type='pay',
                    frequency=1,
                    event_timestamp=timezone.now()
                )
                user_event.save()
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                try:
                    payment = Payment(
                        user_id=request.user.id,
                        payment_id=vnp_TransactionNo,
                        payment_method='VNPAY',
                        amount_paid=amount_usd,
                        status='Completed',
                    )
                    payment.save()
                    order.payment = payment
                    order.is_ordered = True
                    order.save()
                    cart_items = CartItem.objects.filter(user=request.user)
                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = request.user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.order_total = round(order.order_total, 2)
                        orderproduct.ordered = True
                        orderproduct.save()

                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variations.all()
                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.variation.set(product_variation)
                        orderproduct.save()

                        product = Product.objects.get(id=item.product_id)
                        product.stock -= item.quantity
                        product.save()
                    CartItem.objects.filter(user=request.user).delete()
                except CartItem.DoesNotExist:
                    pass
                payments(request, order_id, vnp_TransactionNo)
                order = Order.objects.get(order_number=order_id, is_ordered=True)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                tax = (2 * order.order_total) / 100
                subtotal = order.order_total - tax
                subtotal = round(subtotal, 2)
                grand_total = order.order_total
                tax = round(tax, 2)
                return render(request, "orders/order_complete.html",
                              {  "title": "Kết quả thanh toán",
                                        "result": "Thành công", "order_id": order_id,
                                        "amount": amount,
                                        "order_desc": order_desc,
                                        "vnp_TransactionNo": vnp_TransactionNo,
                                        "vnp_ResponseCode": vnp_ResponseCode,
                                        'user_name': order.user.full_name,
                                        'date': order.date,
                                        'note': order.order_note,
                                        'ordered_products': ordered_products,
                                        'address': order.address,
                                        'subtotal': subtotal,
                                        'tax': tax,
                                        'grand_total': grand_total,
                                        'order_status': order.order_status,
                                        'created_at': order.created_at
                                    })
            else:
                try:
                    payment = Payment(
                        user_id=request.user.id,
                        payment_id=vnp_TransactionNo,
                        payment_method='VNPAY',
                        amount_paid=amount_usd,
                        status='Cancelled',
                    )
                    payment.save()
                    order.payment = payment
                    order.order_status = "Cancelled"
                    order.save()
                    cart_items = CartItem.objects.filter(user=request.user)
                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = request.user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.order_total = round(order.order_total, 2)
                        orderproduct.ordered = False
                        orderproduct.save()

                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variations.all()
                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.variation.set(product_variation)
                        orderproduct.save()

                        product = Product.objects.get(id=item.product_id)
                        product.save()
                    CartItem.objects.filter(user=request.user).delete()
                except CartItem.DoesNotExist:
                    pass

                order = Order.objects.get(order_number=order_id, is_ordered=False)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                tax = (2 * order.order_total) / 100
                subtotal = order.order_total - tax
                subtotal = round(subtotal, 2)
                grand_total = order.order_total
                tax = round(tax, 2)
                return render(request, "orders/order_complete.html",
                              {"title": "Kết quả thanh toán",
                                        "result": "Lỗi", "order_id": order_id,
                                        "amount": amount,
                                        "order_desc": order_desc,
                                        "vnp_TransactionNo": vnp_TransactionNo,
                                        "vnp_ResponseCode": vnp_ResponseCode,
                                        'user_name': order.user.full_name,
                                        'date': order.date,
                                        'note': order.order_note,
                                        'ordered_products': ordered_products,
                                        'address': order.address,
                                        'subtotal': subtotal,
                                        'tax': tax,
                                        'grand_total': grand_total,
                                        'order_status': order.order_status,
                                        'created_at': order.created_at
                                    })
        else:
            try:
                payment = Payment(
                    user_id=request.user.id,
                    payment_id=vnp_TransactionNo,
                    payment_method='VNPAY',
                    amount_paid=round(amount_usd,2),
                    status='Cancelled',
                )
                payment.save()
                order.payment = payment
                order.order_status = "Cancelled"
                order.save()
                cart_items = CartItem.objects.filter(user=request.user)
                for item in cart_items:
                    orderproduct = OrderProduct()
                    orderproduct.order_id = order.id
                    orderproduct.payment = payment
                    orderproduct.user_id = request.user.id
                    orderproduct.product_id = item.product_id
                    orderproduct.quantity = item.quantity
                    orderproduct.product_price = item.product.price
                    orderproduct.order_total = round(order.order_total,2)
                    orderproduct.ordered = False
                    orderproduct.save()

                    cart_item = CartItem.objects.get(id=item.id)
                    product_variation = cart_item.variations.all()
                    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                    orderproduct.variation.set(product_variation)
                    orderproduct.save()

                    product = Product.objects.get(id=item.product_id)
                    product.save()
                CartItem.objects.filter(user=request.user).delete()
            except CartItem.DoesNotExist:
                pass
            order = Order.objects.get(order_number=order_id, is_ordered=False)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)
            tax = (2 * order.order_total) / 100
            subtotal = order.order_total - tax
            subtotal = round(subtotal, 2)
            grand_total = order.order_total
            tax = round(tax, 2)
            return render(request, "orders/order_complete.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum",
                           'user_name': order.user.full_name,
                           'date': order.date,
                           'note': order.order_note,
                           'ordered_products': ordered_products,
                           'address': order.address,
                           'subtotal': subtotal,
                           'tax': tax,
                           'grand_total': grand_total,
                           'order_status': order.order_status,
                           'created_at': order.created_at
                           })
    else:
        return render(request, "orders/order_complete.html", {"title": "Kết quả thanh toán", "result": ""})


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items_ttl = CartItem.objects.filter(user=current_user, is_active=True)
    cart_count = cart_items_ttl.count()
    if cart_count <= 0:
        return redirect('store')

    for cart_items in cart_items_ttl:
        total += (cart_items.product.price * cart_items.quantity)
        quantity += cart_items.quantity

    tax = (2 * total) / 100
    grand_total = total + tax
    order_id = get_formatted_time()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            data = Order()
            data.user = current_user
            data.order_number = order_id
            data.full_name = form.cleaned_data['full_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.road = form.cleaned_data['road']
            data.ward = form.cleaned_data['ward']
            data.district = form.cleaned_data['district']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.payment_method = form.cleaned_data['payment_method']
            data.order_total = round(grand_total, 2)
            data.tax = round(tax, 2)
            data.ip = get_client_ip(request)
            data.save()

            payment_type = data.payment_method
            order_note = form.cleaned_data['order_note']
            if not order_note:
                order_note = "No Note"
            amount = int(grand_total * 100)
            amount_vnd = amount * 25000

            if payment_type == "VNPAY":
                bank_code = request.POST.get('bank_code', '')
                language = "en"
                ipaddr = get_client_ip(request)

                vnp = vnpay()
                vnp.requestData['vnp_Version'] = '2.1.0'
                vnp.requestData['vnp_Command'] = 'pay'
                vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
                vnp.requestData['vnp_Amount'] = amount_vnd
                vnp.requestData['vnp_CurrCode'] = 'VND'
                vnp.requestData['vnp_TxnRef'] = order_id
                vnp.requestData['vnp_OrderInfo'] = order_note
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
            elif payment_type == "COD":
                order = Order.objects.get(order_number=order_id, is_ordered=False)
                if order.is_view == False:
                    return redirect('order_details', order_id=order.order_number)
                try:
                    payment = Payment(
                        user_id=request.user.id,
                        payment_id=0,
                        payment_method='COD',
                        amount_paid=round(grand_total, 2),
                        status='Pending',
                    )
                    payment.save()
                    order.payment = payment
                    order.is_ordered = True
                    order.save()
                    cart_items = CartItem.objects.filter(user=request.user)
                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = request.user.id
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.order_total = round(order.order_total,2)
                        orderproduct.ordered = True
                        orderproduct.save()

                        cart_item = CartItem.objects.get(id=item.id)
                        product_variation = cart_item.variations.all()
                        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                        orderproduct.variation.set(product_variation)
                        orderproduct.save()

                        product = Product.objects.get(id=item.product_id)
                        product.stock -= item.quantity
                        product.save()
                    CartItem.objects.filter(user=request.user).delete()
                except CartItem.DoesNotExist:
                    pass
                payments(request, order_id, 0)
                order = Order.objects.get(order_number=order_id, is_ordered=True)
                ordered_products = OrderProduct.objects.filter(order_id=order.id)
                tax = (2 * order.order_total) / 100
                subtotal = order.order_total - tax
                subtotal = round(subtotal, 2)
                grand_total = order.order_total
                tax = round(tax, 2)
                return render(request, "orders/order_complete.html",
                              {"title": "Kết quả thanh toán",
                                        "result": "Thành công", "order_id": order_id,
                                        "amount": amount,
                                        'user_name': order.user.full_name,
                                        'date': order.date,
                                        'note': order.order_note,
                                        'ordered_products': ordered_products,
                                        'address': order.address,
                                        'subtotal': subtotal,
                                        'tax': tax,
                                        'grand_total': grand_total,
                                        'order_status': order.order_status,
                                        'created_at': order.created_at
                                    })
        else:
            return HttpResponse('Form is not valid')
    else:
        return redirect('checkout')


def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result


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


# @csrf_exempt
# def paymenthandler(request, total=0, quantity=0):
#     # Only accept POST request
#     if request.method == 'POST':
#         try:
#             # get the required parameters from post request
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#
#             result = signature
#             if result is not None:
#                 amount = request.session['razorpay_amount']
#                 print(amount)
#                 try:
#                     razorpay_client.payment.capture(payment_id, amount)
#
#                     # Render Success Page on successfull capture of payment
#
#                     order = Order.objects.get(user=request.user, is_ordered=False, order_number=razorpay_order_id)
#                     print(order)
#                     # Save payment information
#                     payment = Payment(
#                         user=request.user,
#                         payment_id=payment_id,
#                         payment_method='RazorPay',
#                         amount_paid=order.order_total,
#                         status='Completed',
#                     )
#                     payment.save()
#                     print(payment)
#                     order.payment = payment
#                     order.is_ordered = True
#                     order.save()
#                     print("order dw", order)
#
#                     # Move the cart item to order product table
#                     cart_items = CartItem.objects.filter(user=request.user)
#
#                     for item in cart_items:
#                         orderproduct = OrderProduct()
#                         orderproduct.order_id = order.id
#                         orderproduct.payment = payment
#                         orderproduct.user_id = request.user.id
#                         orderproduct.product_id = item.product_id
#                         orderproduct.quantity = item.quantity
#                         orderproduct.product_price = item.product.price
#                         orderproduct.order_total = order.order_total
#                         orderproduct.ordered = True
#                         orderproduct.save()
#
#                         # variations adding to order product
#                         # check variation variable name in orders cart and payment to avido confusing in future
#                         cart_item = CartItem.objects.get(id=item.id)
#                         product_variation = cart_item.variations.all()
#                         orderproduct = OrderProduct.objects.get(id=orderproduct.id)
#                         orderproduct.variation.set(product_variation)
#                         orderproduct.save()
#
#                         # Reduce the quantity of the sold products from orginal stock
#                         product = Product.objects.get(id=item.product_id)
#                         product.stock -= item.quantity
#                         product.save()
#
#                     # Clear the Cart
#                     CartItem.objects.filter(user=request.user).delete()
#                     print("cart cleared")
#
#                     # Send email to the user ( with order details )
#                     mail_subject = 'Thank you for your order.'
#                     message = render_to_string('orders/order_mail.html', {
#                         'user': request.user,
#                         'order': order,
#                         'items': cart_items,
#                         'url': 'http://127.0.0.1:8000/orders/order_complete/?' + 'order_number=' + order.order_number + '&payment_id=' + payment.payment_id,
#
#                     })
#                     to_email = order.email
#                     print(to_email)
#                     send_email = EmailMessage(mail_subject, message, to=[to_email])
#                     send_email.content_subtype = "html"
#                     send_email.send()
#
#                     # Send Transaction Successfull
#                     param = (
#                             "order_number=" + order.order_number + "&payment_id=" + payment.payment_id
#                     )
#                     print(param)
#                     # Capture the payment
#                     return redirect('/orders/order_complete/?' + param)
#
#
#                 except Exception as e:
#                     # If there is an error while capturing payment
#                     messages.error(request, "Payment Failed1")
#                     return HttpResponse("Payment Failed")
#                     return redirect("place_order")
#
#
#             else:
#                 messages.error(request, "Payment Failed2")
#                 return HttpResponse("Payment Failed2")
#                 return redirect("place_order")
#
#                 # if signature verification fails
#
#         except:
#             messages.error(request, "Payment Failed3")
#             return HttpResponse("Payment Failed3")
#             return redirect("place_order")
#
#             # If required parameters in not found in POST data
#
#     else:
#         return redirect("place_order")
#         return HttpResponse("Payment Failed3")
#         # if request is not POST


def add_review(request, id):
    if request.method == "POST":
        return HttpResponse('Form is not valid')