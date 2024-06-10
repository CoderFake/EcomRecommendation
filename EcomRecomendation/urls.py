

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('adminApp.urls')),
    path('', include('homeApp.urls')),
    path('accounts/', include('accounts.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    # orders
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

