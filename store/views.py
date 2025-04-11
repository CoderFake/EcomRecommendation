import io
import logging
import os
import random
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
import numpy as np
import faiss
from accounts.models import EventUser, UserProfile
from carts.views import _cart_id
from carts.models import CartItem
from category.models import CategoryMain, SubCategory
from orders.models import OrderProduct
from store.models import Product
from asgiref.sync import sync_to_async, async_to_sync
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MODEL_IMAGE_DIR = os.path.join(settings.BASE_DIR, 'static', 'model', 'recom_search_image')
embedding_model_path = os.path.join(MODEL_IMAGE_DIR, 'embedding_model.h5')
faiss_path = os.path.join(MODEL_IMAGE_DIR, 'faiss_index.bin')


def get_user_profile(user):
    if user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            profile.save()
        return profile
    return None


def store(request, category_slug=None):
    products = None
    produ_count = 0
    if category_slug:
        if category_slug == "all":
            products = Product.objects.all().order_by('-created_date')
        else:
            category = get_object_or_404(CategoryMain, slug=category_slug)
            products = Product.objects.filter(category_main=category).order_by('-created_date')
    else:
        products = Product.objects.all().order_by('-created_date')
    produ_count = products.count()
    paginator = Paginator(products, 20)  # Hiển thị 20 sản phẩm trên mỗi trang
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    if page_obj.number == paginator.num_pages:
        start = produ_count - ((page_obj.number - 1) * 20)
        end = produ_count
    else:
        start = (page_obj.number - 1) * 20 + 1
        end = start + len(page_obj.object_list) - 1

    context = {
        'page_obj': page_obj,
        'produ_count': produ_count,
        'start': start,
        'end': end
    }

    return render(request, 'store/store.html', context)


def substore(request, category_slug=None, sub_category_slug=None):
    products = None
    produ_count = 0

    if category_slug and sub_category_slug:
        subcategory = get_object_or_404(SubCategory, slug=sub_category_slug)
        products = Product.objects.filter(sub_category=subcategory).order_by('-created_date')
    else:
        products = Product.objects.all().order_by('-created_date')

    produ_count = products.count()

    paginator = Paginator(products, 20)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    if page_obj.number == paginator.num_pages:
        start = produ_count - ((page_obj.number - 1) * 20)
        end = produ_count
    else:
        start = (page_obj.number - 1) * 20 + 1
        end = start + len(page_obj.object_list) - 1

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
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        request.session['product'] = product.id
        if request.user.is_authenticated:
            time_threshold = timezone.now() - timedelta(hours=24)
            event = EventUser.objects.filter(
                user=request.user,
                product=product,
                event_type='view',
                event_timestamp__gte=time_threshold
            ).first()

            if event:
                event.frequency = (event.frequency or 0) + 1
                event.event_timestamp = timezone.now()
                event.save()
            else:
                EventUser.objects.create(
                    user=request.user,
                    product=product,
                    event_type='view',
                    event_timestamp=timezone.now(),
                    frequency=1,
                )
        if request.user.is_authenticated:
            if OrderProduct.objects.filter(product_id=product.id, user_id=request.user.id).exists():
                latest_order_product = OrderProduct.objects.filter(
                    product_id=product.id,
                    user_id=request.user.id
                ).latest('created_at')
                if latest_order_product.reviews.exists():
                    rv = None
        related_products = Product.objects.filter(
            category_main=product.category_main,
            sub_category=product.sub_category
        ).exclude(id=product.id).distinct().order_by('-rating')[:8]

    context = {
        'product': product,
        'in_cart': in_cart,
        'order_product': order_product,
        'related_products': related_products,
        'rv': rv
    }
    return render(request, 'store/product_detail.html', context)


def product_session(request):
    if request.method == 'POST' and 'product_slug' in request.POST:
        product = get_object_or_404(Product, slug=request.POST.get('product_slug', ''))
        if product:
            request.session['product'] = product.id

            if request.user.is_authenticated:
                time_threshold = timezone.now() - timedelta(hours=24)
                event = EventUser.objects.filter(
                    user=request.user,
                    product=product,
                    event_type='view',
                    event_timestamp__gte=time_threshold
                ).first()

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
def get_embedding(model, img_bytes):
    """
    Lấy embedding của ảnh
    """
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

            try:
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
                logging.info(f"Found {len(products_list)} products for the uploaded image.")

            except Exception as e:
                logging.error(f"Error in image search: {e}")
                return redirect('store')

        elif 'keyword' in request.POST:
            keyword = request.POST['keyword']
            products_list = Product.objects.filter(
                Q(product_name__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(short_desp__icontains=keyword)
            ).order_by('-rating')
        produ_count = len(products_list)
        paginator = Paginator(products_list, 20)
        page = request.GET.get('page', 1)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        if page_obj.number == paginator.num_pages:
            start = produ_count - ((page_obj.number - 1) * 20)
            end = produ_count
        else:
            start = (page_obj.number - 1) * 20 + 1
            end = start + len(page_obj.object_list)

        context = {
            'page_obj': page_obj,
            'produ_count': produ_count,
            'start': start,
            'end': end,
            'is_search_result': True
        }

        return render(request, 'store/store.html', context)
    else:
        return redirect('store')