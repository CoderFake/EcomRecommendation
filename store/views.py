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
from carts.models import CartItem, Cart
from category.models import CategoryMain, SubCategory
from orders.models import OrderProduct
from store.models import Product, Variation, Wishlist
from asgiref.sync import sync_to_async, async_to_sync
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MODEL_IMAGE_DIR = os.path.join(settings.BASE_DIR, 'static', 'model', 'recom_search_image')
embedding_model_path = os.path.join(MODEL_IMAGE_DIR, 'embedding_model.h5')
faiss_path = os.path.join(MODEL_IMAGE_DIR, 'faiss_index.bin')

COLOR_MAP = {
    'black': '#000000',
    'white': '#FFFFFF',
    'red': '#FF0000',
    'green': '#00FF00',
    'blue': '#0000FF',
    'yellow': '#FFFF00',
    'purple': '#800080',
    'pink': '#FFC0CB',
    'orange': '#FFA500',
    'brown': '#A52A2A',
    'gray': '#808080',
    'grey': '#808080',
    'navy': '#000080',
    'navy blue': '#000080',
    'light blue': '#ADD8E6',
    'dark blue': '#00008B',
    'light green': '#90EE90',
    'dark green': '#006400',
    'beige': '#F5F5DC',
    'olive': '#808000',
    'maroon': '#800000',
    'coral': '#FF7F50',
    'turquoise': '#40E0D0',
    'teal': '#008080',
    'magenta': '#FF00FF',
    'gold': '#FFD700',
    'silver': '#C0C0C0'
}

def get_color_code(color_name):
    if not color_name:
        return '#000000'
    
    color_lower = color_name.lower()
    
    if color_lower in COLOR_MAP:
        return COLOR_MAP[color_lower]

    for color_key, color_value in COLOR_MAP.items():
        if color_key in color_lower or color_lower in color_key:
            return color_value
    
    return '#000000'


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
    
    categories = CategoryMain.objects.all()
    cat_main_links = CategoryMain.objects.all()
    
    color_filter = request.GET.get('color')
    if color_filter:
        color_variations = Variation.objects.filter(
            Variation_category='Color', 
            Variation_value__icontains=color_filter, 
            is_active=True
        )
        product_ids = color_variations.values_list('Product_id', flat=True)
        products = products.filter(id__in=product_ids)
    
    size_filter = request.GET.get('size')
    if size_filter:
        size_variations = Variation.objects.filter(
            Variation_category='Size', 
            Variation_value__icontains=size_filter, 
            is_active=True
        )
        product_ids = size_variations.values_list('Product_id', flat=True)
        products = products.filter(id__in=product_ids)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)
    
    sort_option = request.GET.get('sort')
    if sort_option:
        if sort_option == 'price_asc':
            products = products.order_by('price')
        elif sort_option == 'price_desc':
            products = products.order_by('-price')
        elif sort_option == 'name_asc':
            products = products.order_by('product_name')
        elif sort_option == 'name_desc':
            products = products.order_by('-product_name')
        elif sort_option == 'rating':
            products = products.order_by('-rating')
        elif sort_option == 'newest':
            products = products.order_by('-created_date')
    
    color_variations = Variation.objects.filter(
        Variation_category='Color',
        is_active=True,
        Product__in=products
    ).values_list('Variation_value', flat=True).distinct()
    
    size_variations = Variation.objects.filter(
        Variation_category='Size',
        is_active=True,
        Product__in=products
    ).values_list('Variation_value', flat=True).distinct()
    
    available_colors = [(color, get_color_code(color)) for color in color_variations]
    
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
        'end': end,
        'categories': categories,
        'cat_main_links': cat_main_links,
        'available_colors': available_colors,
        'available_sizes': size_variations,
        'current_category': category_slug,
        'selected_color': color_filter,
        'selected_size': size_filter,
        'min_price': min_price,
        'max_price': max_price,
        'sort_option': sort_option
    }

    return render(request, 'store/store.html', context)


def substore(request, category_slug=None, sub_category_slug=None):
    products = None
    produ_count = 0
    category = None
    subcategory = None

    if category_slug and sub_category_slug:
        category = get_object_or_404(CategoryMain, slug=category_slug)
        subcategory = get_object_or_404(SubCategory, slug=sub_category_slug)
        products = Product.objects.filter(sub_category=subcategory).order_by('-created_date')
    else:
        products = Product.objects.all().order_by('-created_date')
    
    categories = CategoryMain.objects.all()
    cat_main_links = CategoryMain.objects.all()
    
    color_filter = request.GET.get('color')
    if color_filter:
        color_variations = Variation.objects.filter(
            Variation_category='Color', 
            Variation_value__icontains=color_filter, 
            is_active=True
        )
        product_ids = color_variations.values_list('Product_id', flat=True)
        products = products.filter(id__in=product_ids)
    
    size_filter = request.GET.get('size')
    if size_filter:
        size_variations = Variation.objects.filter(
            Variation_category='Size', 
            Variation_value__icontains=size_filter, 
            is_active=True
        )
        product_ids = size_variations.values_list('Product_id', flat=True)
        products = products.filter(id__in=product_ids)
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    elif min_price:
        products = products.filter(price__gte=min_price)
    elif max_price:
        products = products.filter(price__lte=max_price)
    
    sort_option = request.GET.get('sort')
    if sort_option:
        if sort_option == 'price_asc':
            products = products.order_by('price')
        elif sort_option == 'price_desc':
            products = products.order_by('-price')
        elif sort_option == 'name_asc':
            products = products.order_by('product_name')
        elif sort_option == 'name_desc':
            products = products.order_by('-product_name')
        elif sort_option == 'rating':
            products = products.order_by('-rating')
        elif sort_option == 'newest':
            products = products.order_by('-created_date')
    
    color_variations = Variation.objects.filter(
        Variation_category='Color',
        is_active=True,
        Product__in=products
    ).values_list('Variation_value', flat=True).distinct()
    
    size_variations = Variation.objects.filter(
        Variation_category='Size',
        is_active=True,
        Product__in=products
    ).values_list('Variation_value', flat=True).distinct()
    
    available_colors = [(color, get_color_code(color)) for color in color_variations]

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
        'end': end,
        'categories': categories,
        'cat_main_links': cat_main_links,
        'available_colors': available_colors,
        'available_sizes': size_variations,
        'current_category': category_slug,
        'current_subcategory': sub_category_slug,
        'selected_color': color_filter,
        'selected_size': size_filter,
        'min_price': min_price,
        'max_price': max_price,
        'sort_option': sort_option
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
    if request.method == 'POST' or request.method == 'GET':
        products_list = []
        
        if request.method == 'POST' and 'image' in request.FILES:
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
                
        elif (request.method == 'POST' and 'keyword' in request.POST) or (request.method == 'GET' and 'keyword' in request.GET):
            keyword = request.POST.get('keyword') if request.method == 'POST' else request.GET.get('keyword')
            products_list = Product.objects.filter(
                Q(product_name__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(short_desp__icontains=keyword)
            ).order_by('-rating')
        else:
            return redirect('store')
            
        categories = CategoryMain.objects.all()
        cat_main_links = CategoryMain.objects.all()
        
        color_filter = request.GET.get('color')
        if color_filter:
            color_variations = Variation.objects.filter(
                Variation_category='Color', 
                Variation_value__icontains=color_filter, 
                is_active=True
            )
            product_ids = color_variations.values_list('Product_id', flat=True)
            products_list = products_list.filter(id__in=product_ids)
        
        size_filter = request.GET.get('size')
        if size_filter:
            size_variations = Variation.objects.filter(
                Variation_category='Size', 
                Variation_value__icontains=size_filter, 
                is_active=True
            )
            product_ids = size_variations.values_list('Product_id', flat=True)
            products_list = products_list.filter(id__in=product_ids)
        
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price and max_price:
            products_list = products_list.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products_list = products_list.filter(price__gte=min_price)
        elif max_price:
            products_list = products_list.filter(price__lte=max_price)
        
        sort_option = request.GET.get('sort')
        if sort_option:
            if sort_option == 'price_asc':
                products_list = products_list.order_by('price')
            elif sort_option == 'price_desc':
                products_list = products_list.order_by('-price')
            elif sort_option == 'name_asc':
                products_list = products_list.order_by('product_name')
            elif sort_option == 'name_desc':
                products_list = products_list.order_by('-product_name')
            elif sort_option == 'rating':
                products_list = products_list.order_by('-rating')
            elif sort_option == 'newest':
                products_list = products_list.order_by('-created_date')
        
        color_variations = Variation.objects.filter(
            Variation_category='Color',
            is_active=True,
            Product__in=products_list
        ).values_list('Variation_value', flat=True).distinct()
        
        size_variations = Variation.objects.filter(
            Variation_category='Size',
            is_active=True,
            Product__in=products_list
        ).values_list('Variation_value', flat=True).distinct()
        
        available_colors = [(color, get_color_code(color)) for color in color_variations]
            
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
            'is_search_result': True,
            'categories': categories,
            'cat_main_links': cat_main_links,
            'available_colors': available_colors,
            'available_sizes': size_variations,
            'selected_color': color_filter,
            'selected_size': size_filter,
            'min_price': min_price,
            'max_price': max_price,
            'sort_option': sort_option
        }

        return render(request, 'store/store.html', context)
    else:
        return redirect('store')

# Wishlist views
def wishlist(request):
    """
    Display user's wishlist products
    """
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-created_at')
        categories = CategoryMain.objects.all()
        cat_main_links = CategoryMain.objects.all()
        
        context = {
            'wishlist_items': wishlist_items,
            'categories': categories,
            'cat_main_links': cat_main_links,
        }
        return render(request, 'store/wishlist.html', context)
    else:
        return redirect('login')

def add_to_wishlist(request, product_id):
    """
    Add a product to user's wishlist
    """
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Product has been added to your wishlist' if created else 'Product is already in your wishlist',
                'created': created,
                'count': Wishlist.objects.filter(user=request.user).count()
            })

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('wishlist')
    else:
        return redirect('login')

def remove_from_wishlist(request, product_id):
    """
    Remove a product from user's wishlist
    """
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product=product)
            wishlist_item.delete()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Product has been removed from your wishlist',
                    'count': Wishlist.objects.filter(user=request.user).count()
                })
        except Wishlist.DoesNotExist:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Product is not in your wishlist'
                })
        
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('wishlist')
    else:
        return redirect('login')

def faq(request):
    """
    View for displaying the FAQ page
    """
    cat_main_links = CategoryMain.objects.all()
    cat_sub_links = SubCategory.objects.all()
    
    # Lấy số lượng giỏ hàng
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
    
    cart_count = sum(item.quantity for item in cart_items)
    
    context = {
        'cat_main_links': cat_main_links,
        'cat_sub_links': cat_sub_links,
        'cart_count': cart_count,
    }
    
    return render(request, 'store/faq.html', context)


def terms_condition(request):
    """
    View for displaying the Terms & Conditions page
    """
    cat_main_links = CategoryMain.objects.all()
    cat_sub_links = SubCategory.objects.all()
    
    # Lấy số lượng giỏ hàng
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
    
    cart_count = sum(item.quantity for item in cart_items)
    
    context = {
        'cat_main_links': cat_main_links,
        'cat_sub_links': cat_sub_links,
        'cart_count': cart_count,
    }
    
    return render(request, 'store/terms_condition.html', context)


def track_order(request):
    """
    View for displaying the Order Tracking page
    """
    cat_main_links = CategoryMain.objects.all()
    cat_sub_links = SubCategory.objects.all()
    
    # Lấy số lượng giỏ hàng
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
    
    cart_count = sum(item.quantity for item in cart_items)
    
    context = {
        'cat_main_links': cat_main_links,
        'cat_sub_links': cat_sub_links,
        'cart_count': cart_count,
    }
    
    return render(request, 'store/track_order.html', context)