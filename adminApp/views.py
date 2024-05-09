from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from EcomRecomendation import settings
from accounts.models import Account, UserProfile
from accounts.views import upload_image_to_cloudflare
from django.shortcuts import redirect
from category.models import CategoryMain, SubCategory
from category.forms import SubCategoryForm, CategoryMainForm
from store.models import Product, Variation, VariationManager
from carts.forms import ProductForm
from store.forms import variationForm
from orders.forms import OrderForm, OrderUpdateForm
from django.http import HttpResponse, JsonResponse
from orders.models import Order, OrderProduct, Payment
from django.contrib import messages
import json
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def count_users_logged_in_today():

    timezone.activate(settings.TIME_ZONE)
    today = timezone.now().date()
    users_logged_in_today = Account.objects.filter(last_login__date__gte=today).count()

    return users_logged_in_today

# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.user.is_superuser:
        context ={
            'user_signins': count_users_logged_in_today()
        }
        return render(request, 'adminApp/dashboard.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_infor(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                data = {
                    'date_of_birth': user_profile.date_of_birth.strftime(
                        "%Y-%m-%d") if user_profile.date_of_birth else None,
                    'sex': user_profile.sex,
                    'road': user_profile.road,
                    'ward': user_profile.ward,
                    'district': user_profile.district,
                    'city': user_profile.city,
                    'profile_picture': user_profile.profile_picture,
                    'bio': user_profile.bio
                }
                return JsonResponse(data)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'User profile not found'}, status=404)
        else:
            return JsonResponse({'error': 'You are not authorized to view this page'}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request, only POST method is allowed'}, status=400)


@login_required(login_url='login')
def user_list(request):
    if request.user.is_superuser:
        profiles = UserProfile.objects.all().order_by('-user__date_joined')
        profile_user = UserProfile.objects.get(user__pk=request.user.id)
        context = {
            'profiles': profiles,
            'profile_user': profile_user
        }
        return render(request, 'adminApp/users/user_list.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_profile(request, pk):
    if request.user.is_superuser:
        if request.method == 'POST':
            user = request.user
            profile = UserProfile.objects.get(user__pk=pk)
            user.full_name = request.POST.get('full_name')
            user.username = request.POST.get('user_name')
            user.phone_number = request.POST.get('phone_number')
            user.save()

            # Cập nhật UserProfile
            date_of_birth = request.POST.get('date_of_birth')
            if date_of_birth:
                try:
                    datetime.strptime(date_of_birth, '%Y-%m-%d')  # Validate date format
                    profile.date_of_birth = date_of_birth  # No need to reformat
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

            # Cập nhật mật khẩu, nếu cần
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if old_password and new_password and confirm_password:
                if new_password == confirm_password:
                    if user.check_password(old_password):
                        user.set_password(new_password)
                        user.save()
                    else:
                        messages.error(request, "Old password is incorrect.")
                else:
                    messages.error(request, "New password and confirm password do not match.")

            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile', pk=profile.pk)

        profile = UserProfile.objects.get(user__pk=pk)
        context = {
            'profile': profile,
        }
        return render(request, 'adminApp/users/user_profile.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_delete(request, pk):
    if request.user.is_superuser:
        user = Account.objects.get(pk=pk)
        user.delete()
        return redirect('user_list')
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_block(request, pk):
    if request.user.is_superuser:
        user = Account.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return redirect('user_list')
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def user_unblock(request, pk):
    if request.user.is_superuser:
        user = Account.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return redirect('user_list')
    return HttpResponse('You are not authorized to view this page')


# User based views ends here ##############################################################

# Category based views ##############################################################

@login_required(login_url='login')
def main_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CategoryMainForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('main_category')
        data = SubCategory.objects.all()
        main = CategoryMain.objects.all()
        form = CategoryMainForm()
        context = {
            'main': main,
            'sub': data,
            'form': form,
        }
        return render(request, 'adminApp/Category/MainCategory.html', context)
    return HttpResponse('You are not authorized to view this page')


def main_category_edit(request, pk):
    if request.user.is_superuser:
        main = CategoryMain.objects.get(pk=pk)
        data = SubCategory.objects.all()
        form = CategoryMainForm(instance=main)
        mains = CategoryMain.objects.all()
        if request.method == 'POST':
            form = CategoryMainForm(request.POST, instance=main)
            if form.is_valid():
                form.save()
                return redirect('main_category')
            else:
                print(form.errors)

        context = {
            'main': main,
            'edit_form': form,
            'sub': data,
            'mains': mains,
        }
        return render(request, 'adminApp/Category/MainCategoryedit.html', context)

    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def main_category_delete(request, pk):
    if request.user.is_superuser:
        main = CategoryMain.objects.get(pk=pk)
        main.delete()
        return redirect('main_category')
    return HttpResponse('You are not authorized to view this page')


# Sub Category based views ##############################################################

@login_required(login_url='login')
def sub_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SubCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('sub_category')
        data = SubCategory.objects.all()
        form = SubCategoryForm()
        context = {
            'sub': data,
            'form': form,

        }
        return render(request, 'adminApp/Category/SubCategory.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def sub_category_edit(request, pk):
    sub = SubCategory.objects.get(pk=pk)
    form = SubCategoryForm(instance=sub)
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SubCategoryForm(request.POST, request.FILES, instance=sub)
            if form.is_valid():
                form.save()
                return redirect('sub_category')
            else:
                print(form.errors)

        context = {
            'sub': sub,
            'edit_form': form,
        }
        return render(request, 'adminApp/Category/SubCategoryedit.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def sub_category_delete(request, pk):
    if request.user.is_superuser:
        sub = SubCategory.objects.get(pk=pk)
        sub.delete()
        return redirect('sub_category')
    return HttpResponse('You are not authorized to view this page')


# Product based views ##############################################################

@login_required(login_url='login')
def product_list(request):
    if request.user.is_superuser:
        product = Product.objects.all()
        addProductForm = ProductForm
        if request.method == 'POST':
            addProductForm = ProductForm(request.POST, request.FILES)
            if addProductForm.is_valid():
                addProductForm.save()
                return redirect('product_list')
        context = {
            'product': product,
            'addProduct': addProductForm,
        }
        return render(request, 'adminApp/Products/product_list.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def product_edit(request, pk):
    if request.user.is_superuser:
        Allproduct = Product.objects.all()
        product = Product.objects.get(pk=pk)
        form = ProductForm(instance=product)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_list')
            else:
                print(form.errors)

        context = {
            'product': Allproduct,
            'product_editing': product,
            'edit_form': form,
        }
        return render(request, 'adminApp/Products/product_edit.html', context)
    else:
        return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def product_delete(request, pk):
    if request.user.is_superuser:
        product = Product.objects.get(pk=pk)
        product.delete()
        return redirect('product_list')
    return HttpResponse('You are not authorized to view this page')


# product variations based views ##############################################################

@login_required(login_url='login')
def add_variations(requst):
    if requst.user.is_superuser:
        existing_variations = Variation.objects.all()
        if requst.method == 'POST':
            form = variationForm(requst.POST, requst.FILES)
            if form.is_valid():
                form.save()
                return redirect('add_variations')
        form = variationForm

        context = {
            'existing_variations': existing_variations,
            'form': form,
        }
        return render(requst, 'AdminApp/Variations/add_variations.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def edit_variations(request, pk):
    if request.user.is_superuser:
        existing_variations = Variation.objects.all()
        variation = Variation.objects.get(pk=pk)
        form = variationForm(instance=variation)
        if request.method == 'POST':
            form = variationForm(request.POST, request.FILES, instance=variation)
            if form.is_valid():
                form.save()
                return redirect('add_variations')
            else:
                print(form.errors)

        context = {
            'existing_variations': existing_variations,
            'variation_editing': variation,
            'form': form,
        }
        return render(request, 'adminApp/Variations/edit_variations.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def delete_variations(request, pk):
    if request.user.is_superuser:
        variation = Variation.objects.get(pk=pk)
        variation.delete()
        return redirect('add_variations')
    return HttpResponse('You are not authorized to view this page')


# Orders based views ##############################################################
@login_required(login_url='login')
def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
        order_products = OrderProduct.objects.all()
        print(order_update)
        context = {
            'orders': orders,
            'order_products': order_products,
        }
        return render(request, 'adminApp/Orders/order_list.html', context)
    return HttpResponse('You are not authorized to view this page')


@login_required(login_url='login')
def order_update(request, pk):
    if request.user.is_superuser:
        orders = Order.objects.get(pk=pk)
        update_order = Order.objects.get(pk=pk)
        form = OrderUpdateForm(instance=update_order)
        if request.method == 'POST':
            form = OrderUpdateForm(request.POST, instance=update_order)
            if form.is_valid():
                form.save()
                return redirect('order_list')
            else:
                print(form.errors)

        context = {
            'orders': orders,
            'form': form,
        }
        return render(request, 'adminApp/Orders/order_update.html', context)
    return HttpResponse('You are not authorized to view this page')
