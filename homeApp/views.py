from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from accounts.models import UserProfile, Account, EventUser
from store.models import Product, ProductImage
from django.http import JsonResponse, HttpResponse
import requests
import random


def index(request):
    all_products = Product.objects.all()
    new_products = Product.objects.all().order_by('-created_date')[:8]
    top_rated_products = Product.objects.all().order_by('-rating')[:8]
    if all_products.count() > 12:
        random_products_ids = random.sample(list(all_products.values_list('id', flat=True)), 12)
        random_products = Product.objects.filter(id__in=random_products_ids)
    else:
        random_products = all_products

    context = {
        'new_products': new_products,
        'top_rated_products': top_rated_products,
        'random_products': random_products,
        'is_home': True
    }

    return render(request, 'homePage/home.html', context)


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
