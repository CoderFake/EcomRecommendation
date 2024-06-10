
from django.urls import path
from .import views
from homeApp import urls as Home_App_urls
from django.conf.urls import include

urlpatterns = [
    path('account_infor', views.account_infor, name='account_infor'),
]