from django.http import JsonResponse
from django.shortcuts import render

from accounts.models import Account


# Create your views here.

def account_infor(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'username': 'none'})
        account = Account.objects.filter(id=request.user.id).first()
        return JsonResponse({'username': account.full_name, 'date_joined': account.date_joined}, status=200)

