from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

# import forms here
from .forms import RegistrationForm
from .forms import UserForm
from .forms import UserProfileForm

from django.contrib import messages, auth
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderProduct, Payment
from store.models import Product
from accounts.models import Account, UserProfile
import razorpay
from orders.models import Payment
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.conf import settings
import os
import requests
from decouple import config
from django.core.mail import send_mail

directory = os.path.join(settings.BASE_DIR, 'static', 'webapp', 'assets', 'user')


def get_locations(id, parent_id):
    api_url = "https://member.lazada.vn/locationtree/api/getSubAddressList?countryCode=VN"
    if parent_id:
        api_url += f"&addressId={parent_id}"
    response = requests.get(api_url)
    locations = response.json().get('module', [])
    for location in locations:
        if location.get('id') == id:
            return location.get('name')
    return None


def upload_image_to_cloudflare(image_file, request):
    account_id = config('CL_ID')
    api_token = config('CL_API_TOKEN')
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1"
    files = {
        'file': (f"user{request.user.id}.jpg", image_file.read(), image_file.content_type)
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        for url in response.json()['result']['variants']:
            if 'users' in url:
                return url
        return None
    else:
        print(response.json())
        response.raise_for_status()


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            user = Account.objects.create(username=username, full_name=full_name, email=email, password=password)
            user.phone_number = phone_number
            user.set_password(request.POST['password'])
            user.save()
            userprofile = UserProfile.objects.create(user=user)
            userprofile.save()
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Activate account'
            user.save()

            parameters = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            mail_body = render_to_string('accounts/account_verification_email.html', parameters)
            email = EmailMessage(
                subject=mail_subject,
                body=mail_body,
                from_email=config('EMAIL_HOST_USER'),
                to=[user.email],
            )
            email.content_subtype = "html"
            try:
                email.send()
                messages.success(request, 'Verification email has been sent to your email address.')
            except Exception as e:
                messages.error(request, 'error: ' + str(e))

            return redirect(f'login?command=verification&email={user.email}')

    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return render(request, 'homePage/home.html')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            timezone.activate(settings.TIME_ZONE)
            user_login = Account.objects.get(email=email)
            user_login.last_login = timezone.now()
            user_login.is_login = True
            user_login.save()
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        # item.save()

                    # Geting the product variations by cat id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Geting the product variations by cat id to acces his product variation
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        exising_variation = item.variations.all()
                        ex_var_list.append(list(exising_variation))
                        id.append(item.id)

                    # to get common product variations
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

                    # for item in cart_item:
                    #     item.user = user
                    #     item.save()
            except:
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    return redirect(params['next'])

            except:
                return redirect('/')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    user_login = Account.objects.get(email=request.user.email)
    user_login.is_login = False
    user_login.save()
    auth.logout(request)
    messages.success(request, 'you are logged out.')
    return redirect('login')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')

    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    user = request.user
    orders = Order.objects.order_by('-created_at').filter(user_id=user.id)
    orders_count = orders.count()
    product_ordered = OrderProduct.objects.filter(user_id=user.id).order_by('-created_at')

    context = {
        'profile': user,
        'orders_count': orders_count,
        'user': user,
        'product_ordered': product_ordered,
        'orders': orders,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # reset pasword
            current_site = get_current_site(request)  # this should be imported
            mail_subject = 'Reset your account passowrd.'
            user.save()
            parameters = {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            mail_body = render_to_string('accounts/reset_password_email.html', parameters)
            email = EmailMessage(
                subject=mail_subject,
                body=mail_body,
                from_email=config('EMAIL_HOST_USER'),
                to=[user.email],
            )
            email.content_subtype = "html"
            try:
                email.send()
                messages.success(request, 'Password reset link has been sent to your email.')
            except Exception as e:
                messages.error(request, 'error: ' + str(e))

            return redirect('login')

        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please enter your new password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Password reset link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset successfully.')
            return redirect('login')

        else:
            messages.error(request, 'Password does not match')
            return redirect('resetPassword')
    else:
        template = 'accounts/resetPassword.html'
        return render(request, template)


@login_required(login_url='login')
def changePassword(request):
    user = request.user
    if request.method == 'POST':
        current_password = request.POST['current_password']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            sucess = user.check_password(current_password)
            if sucess:
                user = Account.objects.get(pk=request.user.pk)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password has been Changed, Please login to.')
                return redirect('login')

        else:
            messages.error(request, 'Password does not match')
            return redirect('changePassword')
    else:
        template = 'accounts/changePassword.html'
        return render(request, template)


@login_required(login_url='login')
def user_profile(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        userprofile = UserProfile.objects.create(user=request.user)
        userprofile.save()

    user = request.user
    profile_data = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        user = request.user
        profile = UserProfile.objects.get(user=request.user)
        if not request.POST.get('username'):
            return HttpResponse('Username is required')
        user.full_name = request.POST.get('full_name')
        user.username = request.POST.get('username')
        user.phone_number = request.POST.get('phone_number')
        user.save()

        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            try:
                datetime.strptime(date_of_birth, '%Y-%m-%d')
                profile.date_of_birth = date_of_birth
            except ValueError:
                print("Incorrect date format")

        profile.sex = request.POST.get('sex')
        profile.road = request.POST.get('road')
        profile.ward = request.POST.get('ward')
        profile.district = request.POST.get('district')
        profile.city = request.POST.get('city')
        profile.bio = request.POST.get('bio')

        # Xử lý file ảnh
        if 'profile_picture' in request.FILES:
            try:
                image_url = upload_image_to_cloudflare(request.FILES['profile_picture'], request)
                if image_url is not None:
                    profile.profile_picture = image_url
            except Exception as e:
                messages.error(request, f"Failed to upload image: {str(e)}")

        profile.save()

        if user_form.is_valid() and profile_form.is_valid():
            updated_user = user_form.save()
            updated_userprofile = profile_form.save()
            user_form = UserForm(instance=updated_user)
            profile_form = UserProfileForm(instance= updated_userprofile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': user,
            'profile_data': profile_data,
        }
        return render(request, 'accounts/profile.html', context)
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': user,
        'profile_data': profile_data,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def order_details(request, order_id):

    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    total = 0
    tax = 0

    for item in order_details:
        item_total = item.product_price * item.quantity
        item.tax = (item_total * 2) / 100
        item.total = item_total + item.tax
        tax += item.tax
        total += item.total

    items_count = order_details.count()

    context = {
        'order_detail': order_details,
        'items_count': items_count,
        'order': order,
        'tax': tax,
        'total': total,
    }
    return render(request, 'accounts/order_details.html', context)



# order cancels
@login_required(login_url='login')
def cancel_order(request, order_id):
    order = Order.objects.get(order_number=order_id)
    Payments = Payment.objects.get(order=order)
    order.order_status = 'Cancelled'
    order.save()
    if order.is_ordered == True:
        Payments.status = 'Refunded'
    Payments.save()

    # refund process of stripe
    if str(Payments).__contains__("pay"):
        paymentId = Payments.payment_id
        refund_amount = Payments.amount_paid
        amount = int(refund_amount * 100)


        # addning stock in product
        order_items = OrderProduct.objects.filter(order=order)
        for item in order_items:
            product = Product.objects.get(id=item.product_id)
            product.stock += item.quantity
            product.save()

    order_items = OrderProduct.objects.filter(order=order)
    for item in order_items:
        product = Product.objects.get(id=item.product_id)
        product.stock += item.quantity
        product.save()

    current_site = get_current_site(request)
    mail_subject = 'Your order from Ekka has been cancelled.'
    message = render_to_string('accounts/order_cancel_mail.html', {
        'user': request.user,
        'order': order,
        'url': f'http:/{current_site}/accounts/order_details/' + order.order_number
    })
    to_email = order.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()

    messages.success(request, 'Your order has been cancelled..!')
    return redirect('dashboard')
