import io
import logging
import os
from datetime import timedelta
import random
import faiss
import numpy as np
from PIL import Image
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import connections
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import pandas as pd
from accounts.models import EventUser, UserProfile
from carts.models import CartItem as cart_item
from carts.views import _cart_id
from category.models import CategoryMain, SubCategory
from orders.models import OrderProduct
from store.models import Product
from asgiref.sync import sync_to_async, async_to_sync
from datetime import datetime

today = datetime.today().date()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(settings.BASE_DIR, 'static', 'model', 'recom')
fp_growth = os.path.join(MODEL_DIR, 'fp_growth_result_unique.csv')
te_model = os.path.join(MODEL_DIR, 'te.pkl')


def recom_product(user):
    data = pd.read_csv(fp_growth)

    data['consequents'] = data['consequents'].apply(lambda x: eval(x))

    user_event = EventUser.objects.filter(user=user).order_by('-event_timestamp').first()

    matching_rules = []
    if user_event and user_event.product:
        product = user_event.product
        sub_category = product.sub_category.sub_category_name
        rules = data['antecedents']

        for idx, rule in enumerate(rules):
            if sub_category in rule:
                matching_rules.extend(data['consequents'][idx])

        # Loại bỏ các phần tử trùng lặp
        matching_rules = list(set(matching_rules))
        for rule in matching_rules:
            print(rule)
    return matching_rules


def store(request, category_slug=None):
    products_list = []
    produ_count = 0
    start = 0
    end = 0

    if category_slug:
        if category_slug == "all":
            products_list = Product.objects.all()
            products_list = list(products_list)
        else:
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
        if request.user.is_authenticated:
            subs = recom_product(request.user)
            user_event = EventUser.objects.filter(user=request.user).order_by('-event_timestamp').first()
            if user_event and hasattr(user_event.product, 'gender') and user_event.product.gender:
                gender = user_event.product.gender
            else:
                user_profile = UserProfile.objects.get(user=request.user)
                gender = "Men" if user_profile.sex == "Male" else "Women"
            recom_products = Product.objects.filter(
                sub_category__sub_category_name__in=subs,
                gender=gender
            ).order_by('-rating')
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

                if recom_products.exists():
                    products_list = list(recom_products) + list(related_products)
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
            else:
                products_list = list(recom_products)
        else:
            products_list = list(Product.objects.all().order_by('-rating'))

    products_list = list(set(products_list))

    random.shuffle(products_list)

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
    return render(request, 'store/store.html', context)


def send_user_events(request):
    if request.method == 'GET':
        # Lấy ngày hiện tại
        today = datetime.today().date()

        # Truy vấn dữ liệu từ Django models, lọc các sự kiện xảy ra trong ngày hôm nay
        events = EventUser.objects.filter(
            event_type__in=['view', 'cart', 'pay'],
            event_timestamp__date=today
        ).values(
            'user_id', 'product_id', 'event_timestamp', 'event_type',
            'product__category_main__category_name', 'product__sub_category__sub_category_name'
        )
        events_df = pd.DataFrame(list(events))

        events_df.rename(columns={
            'product__category_main__category_name': 'main_category_name',
            'product__sub_category__sub_category_name': 'sub_category_name'
        }, inplace=True)


        pre_train_path = f'{MODEL_DIR}/pre_train.csv'
        os.makedirs(os.path.dirname(pre_train_path), exist_ok=True)
        events_df.to_csv(pre_train_path, index=False)

        pre_train_df = pd.read_csv(pre_train_path)
        pre_train_json = pre_train_df.to_json(orient='records')

        response = requests.post('http://localhost:5001/update_user_events', json={'data': pre_train_json})

        if response.status_code == 200:
            save_path = f'{MODEL_DIR}/fp_growth_result_unique.csv'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'wb') as f:
                f.write(response.content)

            return JsonResponse({'status': 'success', 'message': 'Data sent to Flask server and file saved successfully.'})
        else:
            return JsonResponse({'status': 'fail', 'message': 'Failed to send data to Flask server.'})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'})


def api_product(request):
    products = Product.objects.all().values()
    products_list = list(products)
    return JsonResponse(products_list, safe=False)


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

        paginator = Paginator(products, 100)
        page = request.GET.get('page')
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

        related_products = Product.objects.filter(
            Q(category_main=product.category_main),
            Q(sub_category=product.sub_category),
            Q(brand_name=product.brand_name),
            Q(gender=product.gender),
            Q(season=product.season),
        ).exclude(id=product.id).distinct().order_by('-rating')[:8]

    context = {
        'product': product,
        'in_cart': in_cart,
        'order_product': order_product,
        'related_products': related_products,
        'rv': rv
    }
    return render(request, 'store/product_detail.html', context)


# Hàm để lấy embedding của ảnh
def get_embedding(model, img_bytes):
    try:
        img = Image.open(img_bytes)
        img = img.convert('RGB')
        img = img.resize((224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        embedding = model.predict(x).reshape(-1)
        return embedding
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None


def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    return embedding / norm

MODEL_IMAGE_DIR = os.path.join(settings.BASE_DIR, 'static', 'model', 'recom_search_image')
embedding_model_path = os.path.join(MODEL_IMAGE_DIR, 'embedding_model.h5')
faiss_path = os.path.join(MODEL_IMAGE_DIR, 'faiss_index.bin')

def get_embedding(model, img_bytes):
    try:
        img = Image.open(img_bytes)
        img = img.convert('RGB')
        img = img.resize((224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        embedding = model.predict(x).reshape(-1)
        return embedding
    except Exception as e:
        logging.error(f"Error processing image: {e}")
        return None


def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    return embedding / norm


MODEL_IMAGE_DIR = os.path.join(settings.BASE_DIR, 'static', 'model', 'recom_search_image')

embedding_model_path = os.path.join(MODEL_IMAGE_DIR, 'embedding_model.h5')
faiss_path = os.path.join(MODEL_IMAGE_DIR, 'faiss_index.bin')

@sync_to_async
def fetch_image_ids(faiss_ids):
    with connections['image_embeddings'].cursor() as cursor:
        placeholders = ','.join(['%s'] * len(faiss_ids))
        query = f"SELECT image_id FROM embeddings WHERE faiss_id IN ({placeholders})"
        cursor.execute(query, faiss_ids)
        return [row[0] for row in cursor.fetchall()]

def chunked_iterable(iterable, size):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

def search(request):
    if request.method == 'POST':
        products_list = []
        if 'image' in request.FILES:
            image_file = request.FILES['image']

            img_bytes = io.BytesIO(image_file.read())

            model = load_model(embedding_model_path)
            index = faiss.read_index(faiss_path)

            embedding = get_embedding(model, img_bytes)
            if embedding is None:
                return redirect('store')

            normalized_embedding = normalize_embedding(embedding)

            D, I = index.search(np.array([normalized_embedding], dtype=np.float32), 100)

            faiss_ids = I[0].tolist()
            product_ids = []
            for chunk in chunked_iterable(faiss_ids, 10):
                product_ids += async_to_sync(fetch_image_ids)(chunk)

            products_list = Product.objects.filter(id__in=product_ids)
            print(f"Found {len(products_list)} products for the uploaded image.")

        elif 'keyword' in request.POST:
            keyword = request.POST['keyword']
            products_list = Product.objects.filter(Q(slug__icontains=keyword) | Q(description__icontains=keyword)).order_by('-rating')

        products_list = list(products_list)
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
        return render(request, 'store/store.html', context)
    else:
        return redirect('store')
