from django.contrib import admin
from .models import Product, Variation, FolderEvent
import json
import requests
from django.http import JsonResponse
from adminApp.views import encrypt, decrypt
from decouple import config
# Register your models here.

class Product_modeladmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'stock', 'is_available', 'category_main', 'sub_category')
    list_filter = ('product_name', 'price', 'stock', 'is_available', 'category_main', 'sub_category')
    search_fields = (
    'product_name', 'slug', 'price', 'description', 'stock', 'is_available', 'category_main', 'sub_category',)

    filter_horizontal = ()
    list_per_page = 25


admin.site.register(Product, Product_modeladmin)


class Variation_modeladmin(admin.ModelAdmin):
    list_display = ('Product', 'Variation_category', 'Variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('Product', 'Variation_category', 'Variation_value', 'is_active')
    search_fields = ('Product', 'Variation_category', 'Variation_value', 'is_active')

    filter_horizontal = ()

    list_per_page = 25


admin.site.register(Variation, Variation_modeladmin)

class FolderEvent_modeladmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    actions = ['get_folders', 'process_folder']

    def get_folders(self, request, queryset):
        response = requests.get(config('GET'))
        if response.status_code == 200:
            data = response.json()
            decrypted_folders = [decrypt(folder) for folder in data['folders']]
            self.message_user(request, f"Folders: {', '.join(decrypted_folders)}")
        else:
            self.message_user(request, "Failed to get folders", level='error')
    get_folders.short_description = "Get Folders from Flask"

    def process_folder(self, request, queryset):
        for event in queryset:
            encrypted_folder_name = encrypt(json.dumps({"folder_name": event.name}))
            response = requests.post(config('POST'), json={"data": encrypted_folder_name})
            if response.status_code == 200:
                self.message_user(request, f"Successfully processed folder {event.name}")
            else:
                self.message_user(request, f"Failed to process folder {event.name}", level='error')
    process_folder.short_description = "Process Folder in Flask"

admin.site.register(FolderEvent, FolderEvent_modeladmin)