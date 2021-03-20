from django.contrib import admin
from django.db.models import Sum, DecimalField, F
from import_export.admin import ExportMixin

from .models import Order, OrderItem
from .resources import OrderResource


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


class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource
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

    def get_export_queryset(self, request):
        return super().get_export_queryset(request).annotate(
            total_revenue=Sum(
                (F('items__price') * F('items__quantity')) - F('discount'),
                output_field=DecimalField()
            )
        ).order_by('id')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
