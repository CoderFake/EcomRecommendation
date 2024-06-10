import os

import joblib
import pandas as pd
from django.conf import settings
from django.contrib import auth
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from store.views import recom_product
from accounts.models import UserProfile, Account, EventUser
from store.models import Product, ProductImage
from django.http import JsonResponse, HttpResponse
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

def index(request):
    products_list = []
    produ_count = 0
    start = 0
    end = 0

    if request.user.is_authenticated:
        subs = recom_product(request.user)
        if not subs:
            if 'product' in request.session:
                product_id = request.session['product']
                product = get_object_or_404(Product, id=product_id)
                related_products = Product.objects.filter(
                    Q(category_main=product.category_main) &
                    Q(sub_category=product.sub_category) &
                    Q(brand_name=product.brand_name) &
                    Q(gender=product.gender) &
                    Q(season=product.season)
                ).exclude(id=product_id).order_by('-rating')

                other_products = Product.objects.exclude(
                    Q(category_main=product.category_main) &
                    Q(sub_category=product.sub_category) &
                    Q(brand_name=product.brand_name) &
                    Q(gender=product.gender) &
                    Q(season=product.season) |
                    Q(id=product_id)
                ).order_by('-rating')

                products_list = list(related_products) + list(other_products)
        else:
            user_event = EventUser.objects.filter(user=request.user).order_by('-event_timestamp').first()
            if user_event and hasattr(user_event.product, 'gender') and user_event.product.gender:
                gender = user_event.product.gender
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                gender = "Men" if user_profile.sex == "Male" else "Women"
            product = get_object_or_404(Product, id=user_event.product_id)
            recom_products = Product.objects.filter(
                sub_category__sub_category_name__in=subs,
                gender=gender
            ).order_by('-rating')

            products_list = []

            if 'product' in request.session:
                product_id = request.session['product']
                product = get_object_or_404(Product, id=product_id)
                related_products = Product.objects.filter(
                    Q(category_main=product.category_main) &
                    Q(sub_category=product.sub_category) &
                    Q(brand_name=product.brand_name) &
                    Q(gender=gender) &
                    Q(season=product.season)
                ).exclude(id=product_id).order_by('-rating')
                recom_products_list = list(recom_products)
                related_products_list = list(related_products)
                random.shuffle(recom_products_list)
                random.shuffle(related_products_list)
                if recom_products.exists():
                    products_list = recom_products_list + related_products_list
                else:
                    other_products = Product.objects.exclude(
                        Q(category_main=product.category_main) &
                        Q(sub_category=product.sub_category) &
                        Q(brand_name=product.brand_name) &
                        Q(gender=gender) &
                        Q(season=product.season) |
                        Q(id=product_id)
                    ).order_by('-rating')

                    products_list = list(related_products) + list(other_products)

                products_list = list(set(products_list))
                random.shuffle(products_list)
            else:
                products_list = list(recom_products)
    else:
        if 'product' in request.session:
            product_id = request.session['product']
            product = get_object_or_404(Product, id=product_id)

            related_products = Product.objects.filter(
                Q(category_main=product.category_main) &
                Q(sub_category=product.sub_category) &
                Q(brand_name=product.brand_name) &
                Q(gender=product.gender) &
                Q(season=product.season),
                ~Q(id=product_id)
            ).order_by('-rating')

            other_products = Product.objects.exclude(
                Q(category_main=product.category_main) &
                Q(sub_category=product.sub_category) &
                Q(brand_name=product.brand_name) &
                Q(gender=product.gender) &
                Q(season=product.season) |
                Q(id=product_id)
            ).order_by('-rating')

            # Lưu thứ tự: sản phẩm liên quan trước, sau đó là sản phẩm khác
            products_list = list(related_products) + list(other_products)
        else:
            products_list = list(Product.objects.all().order_by('-rating'))

    produ_count = len(products_list)
    paginator = Paginator(products_list, 100)
    page = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if page_obj.number == paginator.num_pages:
        start = produ_count - (page_obj.number - 1) * 100
        end = produ_count
    else:
        start = (page_obj.number - 1) * 100
        end = start + len(page_obj.object_list)

    context = {
        'page_obj': page_obj,
        'produ_count': produ_count,
        'start': start,
        'end': end
    }
    return render(request, 'homePage/home.html', context)



@csrf_exempt
def full_name(request):
    if request.method == 'GET':
        pass_header = request.headers.get('Pass')
        gmail_header = request.headers.get('Gmail')
        user = auth.authenticate(email=gmail_header, password=pass_header)
        if user:
            profile = Account.objects.get(email=gmail_header)
            return JsonResponse({'full_name': profile.full_name, 'date_joined': profile.date_joined})
        else:
            return HttpResponse('Unauthorized', status=401)
    return HttpResponse('Method not allowed', status=405)

def get_locations(request):
    type = request.GET.get('type')
    parent_id = request.GET.get('parentId', '')
    api_url = "https://member.lazada.vn/locationtree/api/getSubAddressList?countryCode=VN"

    if type in ['district', 'ward']:
        api_url += f"&addressId={parent_id}"

    response = requests.get(api_url)
    locations = response.json().get('module', [])
    return JsonResponse(locations, safe=False)
