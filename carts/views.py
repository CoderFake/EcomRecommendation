from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import UserProfile, EventUser
from store.models import Product as Prouct_modle, Variation
from .models import Cart, CartItem
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def get_formatted_time():
    now = timezone.now()
    formatted_time = now.strftime('%Y%m%d%H%M%S')
    return formatted_time

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='login')
def update_cart(request):
    if request.method == 'POST':
        data = request.POST
        cart_item_id = data.get('cartItemId')
        new_quantity = int(data.get('quantity'))

        cart_item = CartItem.objects.get(id=cart_item_id)
        if cart_item and new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
            sub_total = cart_item.sub_total()
            return JsonResponse({'success': True, 'sub_total': sub_total, 'quantity': new_quantity})
        else:
            return JsonResponse({'success': False})

def add_cart(request, product_id):
    current_user = request.user
    product = Prouct_modle.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            event = EventUser.objects.filter(user_id=request.user.id, product_id = product_id, event_type='cart')
            if event:
                event.frequency += 1
                event.event_timestamp = timezone.now()
                event.save()
            else:
                user_event = EventUser(
                    user_id=request.user.id,
                    product_id=product_id,
                    event_type='cart',
                    frequency=1,
                    event_timestamp=timezone.now()
                )
                user_event.save()

            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(Product=product, Variation_category__iexact=key,
                                                      Variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()


            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                item.save()

                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:  # ,
                    variation = Variation.objects.get(Product=product, Variation_category__iexact=key,
                                                      Variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                item.save()

                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)

                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Prouct_modle, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Prouct_modle, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity


    except ObjectDoesNotExist:
        pass

    tax_percentage = 2
    tax = (tax_percentage * total) / 100
    grand_total = total + tax
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax_percentage': tax_percentage,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True).prefetch_related("user")
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity


    except ObjectDoesNotExist:
        HttpResponse('You have no items in your cart')

    profile = UserProfile.objects.get(user=request.user)
    tax_percentage = 2
    tax = (tax_percentage * total) / 100
    grand_total = total + tax
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax_percentage': tax_percentage,
        'tax': tax,
        'grand_total': grand_total,
        'profile': profile
    }

    return render(request, 'store/checkout.html', context)
