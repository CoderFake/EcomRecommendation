import os
import pandas as pd
import numpy as np
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from store.models import Product
from accounts.models import EventUser
from category.models import CategoryMain, SubCategory
from carts.views import _cart_id
from carts.models import CartItem as cart_item
from orders.models import Order
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from orders.models import OrderProduct
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from django.utils import timezone
from datetime import timedelta
import joblib

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
#
#
# def calculate_total_spent_by_user(user_id):
#
#     completed_orders = Order.objects.filter(user_id=user_id, status='Completed')
#     total_spent = completed_orders.aggregate(total_amount_spent=Sum('order_total'))
#     if total_spent.get('total_amount_spent') is None:
#         return 0
#     return 0
# def find_similar_products(user_id):
#     event_count = EventUser.objects.filter().count()
#     if event_count < 8:
#         return False
#     latest_events = EventUser.objects.filter().order_by('-event_timestamp')
#
#     total_spent = calculate_total_spent_by_user(user_id)
#
#     data = pd.DataFrame(list(latest_events.values('event_type', 'event_timestamp', 'frequency', 'rating', 'product_id')))
#     data['event_timestamp'] = pd.to_datetime(data['event_timestamp'])
#
#     # Tính toán các đặc điểm cần thiết
#     data['time_of_day'] = pd.cut(data['event_timestamp'].dt.hour, bins=[0, 3, 6, 9, 12, 15, 18, 21, 24],
#                                  labels=['0-3', '3-6', '6-9', '9-12', '12-15', '15-18', '18-21', '21-24'], right=False)
#     data['day_type'] = data['event_timestamp'].dt.day_name().apply(
#         lambda x: 'weekend' if x in ['Saturday', 'Sunday'] else 'normal_day')
#     data['day_type_encoded'] = day_encoder.transform(data['day_type'])
#     data['time_of_day_encoded'] = time_encoder.transform(data['time_of_day'])
#     data['frequency_scaled'] = frequency_scaler.transform(data[['frequency']])
#     features_aggregated = data[['time_of_day_encoded', 'day_type_encoded', 'frequency_scaled']].mean().to_frame().T
#     features_aggregated['user_id'] = user_id
#
#     views = data[data['event_type'] == 'view'].shape[0]
#     pays = data[data['event_type'] == 'pay'].shape[0]
#     if views > 0:
#         purchase_ratio = pays / views
#     else:
#         purchase_ratio = 0
#
#     average_rating = data['rating'].mean()
#     product_diversity = data['product_id'].nunique()
#
#     features = pd.DataFrame({
#         'total_spent': [total_spent],
#         'purchase_ratio': [purchase_ratio],
#         'average_rating': [average_rating],
#         'product_diversity': [product_diversity],
#         'user_id': [user_id]
#     })
#     print(features)
#
#     features[['total_spent_scaled', 'purchase_ratio_scaled']] = user_scaler.transform(features[['total_spent', 'purchase_ratio']])
#     features['user_id'] = user_id
#     features_combined = features.merge(features_aggregated, on='user_id', how='left')
#
#     features_combined.replace([np.inf, -np.inf], np.nan, inplace=True)
#     features_combined.dropna(inplace=True)
#
#     user_clusters = user_model.predict(features_combined.drop(columns=["user_id"]))
#     recom_user_cluster = user_clusters[0]

    # user_events = EventUser.objects.filter(user_id=user_id).order_by('-event_timestamp')[:20]
    # product_ids = user_events.values_list('product_id', flat=True)
    # products = Product.objects.filter(id__in=product_ids)
    # products = list(products.values())
    # filtered_products = [{k: v for k, v in product.items() if k != 'description'} for product in products]
    # product_data = pd.DataFrame(filtered_products)
    # selected_columns = ['brand_name', 'gender', 'price', 'rating', 'season', 'category_main_id', 'sub_category_id']
    # product_features = product_data[selected_columns]
    #
    # product_features['brand_name'] = brand_name_encoder.transform(product_features['brand_name'])
    # product_features['gender'] = gender_encoder.transform(product_features['gender'])
    # product_features['season'] = season_encoder.transform(product_features['season'])
    # product_features[['price', 'rating', 'category_main_id', 'sub_category_id']] = product_scaler.transform(
    #     product_features[['price', 'rating', 'category_main_id', 'sub_category_id']])

    # user_product_clusters = product_model.predict(product_features)
    # recommended_cluster = interaction_matrix.loc[recom_user_cluster].idxmax()
    # similar_products_ids = product_matrix[product_matrix['product_cluster'] == recommended_cluster]['product_id']
    # similar_products = Product.objects.filter(id__in=similar_products_ids, is_available=True).order_by('-rating')
    #
    # return similar_products


def product_session(request):
    if request.method == 'POST' and 'product_slug' in request.POST:
        product = get_object_or_404(Product, slug=request.POST.get('product_slug', ''))
        if product:
            request.session['product'] = product.id

            if request.user.is_authenticated:
                time_threshold = timezone.now() - timedelta(hours=24)
                event = EventUser.objects.filter(user=request.user, product=product, event_type='view',
                                                 event_timestamp__gte=time_threshold).first()

                if event:
                    # Nếu có sự kiện, tăng frequency và cập nhật timestamp
                    event.frequency = (event.frequency or 0) + 1
                    event.event_timestamp = timezone.now()
                    event.save()
                    return HttpResponse("Success: View event updated")
                else:
                    EventUser.objects.create(
                        user=request.user,
                        product=product,
                        event_type='view',
                        event_timestamp=timezone.now(),
                        frequency=1,
                    )
                    return HttpResponse("Success: View event created")
            else:
                return HttpResponse("User not authenticated", status=403)
        else:
            return HttpResponse("Product not found", status=404)
    else:
        return HttpResponse("Invalid request", status=400)


def store(request, category_slug=None):
    products_list = []
    produ_count = 0
    start = 0
    end = 0

    if category_slug:
        category = get_object_or_404(CategoryMain, slug=category_slug)
        if 'product' in request.session:
            product_id = request.session['product']
            related_products = None
            product = get_object_or_404(Product, id=product_id)
            if product.category_main.slug == category_slug:
                related_products = Product.objects.filter(
                    Q(category_main=product.category_main) &
                    Q(sub_category=product.sub_category) &
                    Q(brand_name=product.brand_name) &
                    Q(gender=product.gender) &
                    Q(season=product.season)
                ).exclude(id=product_id).order_by('-rating')

                other_products = Product.objects.filter(category_main=category).exclude(
                    id__in=related_products.values_list('id', flat=True)
                ).order_by('-rating')
                products_list = list(related_products) + list(other_products)
            else:
                products_list = list(Product.objects.filter(category_main=category).order_by('-rating'))
        else:
            products_list = list(Product.objects.filter(category_main=category).order_by('-rating'))
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
    paginator = Paginator(products_list, 100)  # Sử dụng danh sách sản phẩm cho phân trang
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
    return render(request, 'store/store.html', context)


def substore(request, category_slug=None, sub_category_slug=None):
    categories = None
    products = None
    start = 0
    end = 0
    if category_slug != None:
        if sub_category_slug != None:
                categories = get_object_or_404(SubCategory, slug=sub_category_slug)
                products = Product.objects.filter(sub_category=categories)
                produ_count = products.count()

                paginator = Paginator(products, 100)  # Hiển thị 100 sản phẩm trên mỗi trang
                page = request.GET.get('page')  # lấy số trang từ query parameters
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    if page == "-1":
                        page_obj = paginator.page(paginator.num_pages)
                    else:
                        page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)

        else:
            products = Product.objects.prefetch_related('images').filter(images__image_type='default').order_by(
                '-rating')
            produ_count = products.count()

        paginator = Paginator(products, 100)  # Hiển thị 100 sản phẩm trên mỗi trang
        page = request.GET.get('page')  # lấy số trang từ query parameters
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            if page == "-1":
                page_obj = paginator.page(paginator.num_pages)
            else:
                page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        if page_obj.number == paginator.num_pages:
            start = produ_count - 100
            end = produ_count
        elif page_obj.object_list.count() == 100 and page_obj.number > 1:
            print(page_obj.number)
            start = page_obj.number * 100 - page_obj.object_list.count()
            end = start + page_obj.object_list.count()
        else:
            start = 0
            end = page_obj.object_list.count()

    context = {
        'page_obj': page_obj,
        'produ_count': produ_count,
        'start': start,
        'end': end
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug=None, sub_category_slug=None, product_slug=None):
    product = None
    in_cart = None
    related_products = None
    rv = "disabled"
    order_product = None

    if product_slug:
        product = get_object_or_404(Product, slug=product_slug)
        in_cart = cart_item.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

        if OrderProduct.objects.filter(product_id=product.id).exists():
            latest_order_product = OrderProduct.objects.filter(product_id=product.id, user_id=request.user.id).latest(
                'created_at')
            if latest_order_product.reviews.exists():
                rv = None

        # Query for similar products
        related_products = Product.objects.filter(
            Q(category_main=product.category_main),
            Q(sub_category=product.sub_category),
            Q(brand_name=product.brand_name),
            Q(gender=product.gender),
            Q(season=product.season),
            Q(rating=5) | Q(rating=4)
        ).exclude(id=product.id).distinct()[:8]

    context = {
        'product': product,
        'in_cart': in_cart,
        'order_product': order_product,
        'related_products': related_products,
        'rv': rv
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products_list = Product.objects.filter(Q(slug__icontains=keyword) | Q(description__icontains = keyword)).order_by('-rating')
        products_list = list(products_list)
        produ_count = len(products_list)
        paginator = Paginator(products_list, 100)  # Sử dụng danh sách sản phẩm cho phân trang
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
        return render(request, 'store/store.html', context)
    else:
        return redirect('store')

