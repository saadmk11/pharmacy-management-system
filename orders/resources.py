from import_export import resources
from import_export.fields import Field

from .models import Order


class OrderResource(resources.ModelResource):
    total = Field(attribute='total', column_name='total', readonly=True)
    order_status = Field(
        attribute='get_order_status_display'
    )
    payment_status = Field(
        attribute='get_payment_status_display'
    )

    class Meta:
        model = Order
        widgets = {
            'created_at': {'format': '%d-%m-%Y'},
            'updated_at': {'format': '%d-%m-%Y'}
        }
        fields = (
            'id', 'customer_name', 'contact_no',
            'discount', 'payment_status', 'order_status',
            'total', 'created_at', 'updated_at',
        )
        export_order = fields