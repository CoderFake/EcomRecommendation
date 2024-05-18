import os

import joblib
import pandas as pd
from django.conf import settings
from django.contrib import auth
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from accounts.models import UserProfile, Account
from store.models import Product, ProductImage
from django.http import JsonResponse, HttpResponse
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def index(request):
    products_list = []
    if 'product' in request.session:
        product_id = request.session['product']
        # if request.user.is_authenticated:
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

        products_list = list(related_products) + list(other_products)
        # else:
        #     if find_similar_products(request.user.id):
        #         products_list = find_similar_products(request.user.id)
        #     else:
        #         products_list = list(Product.objects.all().order_by('-rating'))
    else:
        products_list = list(Product.objects.all().order_by('-rating'))

    paginator = Paginator(products_list, 100)
    page = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
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
