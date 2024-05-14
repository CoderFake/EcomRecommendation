
from django.urls import path, include
from django.conf.urls.static import static
from .import views


urlpatterns = [
    path('payment_ipn/', views.payment_ipn, name='payment_ipn'),
    path('place_order/', views.place_order, name='place_order'),
    path('', views.add_review, name='add_review'),
    path('payment_return/', views.payment_return, name='order_complete'),
] 
