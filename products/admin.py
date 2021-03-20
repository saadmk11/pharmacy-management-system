from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
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
        'price'
    ]


admin.site.register(Product, ProductAdmin)
