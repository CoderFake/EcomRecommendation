import os

import joblib
import pandas as pd
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from store.models import Product, ProductImage
from django.http import JsonResponse
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from store.views import find_similar_products
#
# MODEL_DIR = os.path.join(settings.BASE_DIR, 'static', 'model', 'recom_product')
#
# user_model_path = os.path.join(MODEL_DIR, 'user_kmeans_model.pkl')
# user_model = joblib.load(user_model_path)
# product_model_path = os.path.join(MODEL_DIR, 'product_kmeans_model.pkl')
# product_model = joblib.load(product_model_path)
#
# day_encoder_path = os.path.join(MODEL_DIR, 'le_day_type.pkl')
# time_encoder_path = os.path.join(MODEL_DIR, 'le_time_of_day.pkl')
# frequency_scaler_path = os.path.join(MODEL_DIR, 'frequency_scaler.pkl')
#
# brand_name_encoder_path = os.path.join(MODEL_DIR, 'brand_name.pkl')
# gender_encoder_path = os.path.join(MODEL_DIR, 'gender.pkl')
# season_encoder_path = os.path.join(MODEL_DIR, 'season.pkl')
# user_scaler_path = os.path.join(MODEL_DIR, 'user_scaler.pkl')
# product_scaler_path = os.path.join(MODEL_DIR, 'product_scaler.pkl')
# product_matrix_path = os.path.join(MODEL_DIR, 'product_matrix.csv')
# cluster_matrix_path = os.path.join(MODEL_DIR, 'cluster_interaction_matrix.csv')
#
# day_encoder = joblib.load(day_encoder_path)
# time_encoder = joblib.load(time_encoder_path)
#
# brand_name_encoder = joblib.load(brand_name_encoder_path)
# gender_encoder = joblib.load(gender_encoder_path)
# season_encoder = joblib.load(season_encoder_path)
# frequency_scaler = joblib.load(frequency_scaler_path)
# user_scaler = joblib.load(user_scaler_path)
# product_scaler = joblib.load(product_scaler_path)
# product_matrix = pd.read_csv(product_matrix_path)
# interaction_matrix = pd.read_csv(cluster_matrix_path)


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


def get_locations(request):
    type = request.GET.get('type')
    parent_id = request.GET.get('parentId', '')
    api_url = "https://member.lazada.vn/locationtree/api/getSubAddressList?countryCode=VN"

    if type in ['district', 'ward']:
        api_url += f"&addressId={parent_id}"

    response = requests.get(api_url)
    locations = response.json().get('module', [])
    return JsonResponse(locations, safe=False)
