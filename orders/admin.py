from django.contrib import admin

from .models import Order, OrderItem

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    search_fields = [
        'order__id',
        'order__contact_no',
        'order__customer_name',
        'product__name',
        'product'
    ]
    list_display = [
        'id',
        'order_id',
        'quantity',
        'price',
        'item_total',
    ]
    autocomplete_fields = ['product']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']
    readonly_fields = ['price']


class OrderAdmin(admin.ModelAdmin):
    search_fields = [
        'items__product__name',
        'items__product__sku_id',
        'id',
        'contact_no',
        'customer_name'
    ]
    list_display = [
        'id',
        'customer_name',
        'contact_no',
        'total_quantity',
        'sub_total',
        'total',
        'order_status',
        'payment_status',
        'created_at',
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_filter = ['payment_status', 'order_status']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
