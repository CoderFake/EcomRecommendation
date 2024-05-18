from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/full_name/', views.full_name, name='full_name'),
    path('api/getLocations/', views.get_locations, name='get_locations'),
]
