from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Product
from .resources import ProductResource


class ProductAdmin(ImportExportModelAdmin):
    model = Product
    resource_class = ProductResource
    search_fields = [
        'id',
        'sku_id',
        'name',
        'description'
    ]
    list_display = [
        'id',
        'name',
        'sku_id',
        'price',
        'is_available'
    ]
    list_editable = [
        'price',
        'is_available'
    ]
    list_filter = [
        'is_available'
    ]
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Product, ProductAdmin)
