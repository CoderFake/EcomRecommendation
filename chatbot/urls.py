from django.urls import path
from . import views
from homeApp import urls as Home_App_urls
from django.conf.urls import include

urlpatterns = [
    path('account_infor', views.account_infor, name='account_infor'),
    path('chat', views.chat_view, name='chat_view'),
    path('generate', views.generate_response, name='generate_response'),
    path('get_initial_message', views.get_initial_message, name='get_initial_message'),
    path('new_chat', views.new_chat_session, name='new_chat_session'),
    path('history/<uuid:session_id>', views.get_chat_history, name='get_chat_history'),
    path('check_auth', views.check_auth, name='check_auth'),
    path('update_session', views.update_session, name='update_session'),
]