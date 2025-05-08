from django.urls import path, include
from django.conf.urls.static import static
from .import views


urlpatterns = [
    path('',views.store, name='store'),
    path('product_session/',views.product_session, name='product_session'),
    path('search/',views.search, name='search'),
    path('wishlist/',views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/',views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/',views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<slug:category_slug>/',views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:sub_category_slug>/',views.substore, name='products_by_sub_category'),
    path('<slug:category_slug>/<slug:sub_category_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),
    path('faq/', views.faq, name='faq'),
    path('terms-condition/', views.terms_condition, name='terms_condition'),
    path('track-order/', views.track_order, name='track_order'),
] 
