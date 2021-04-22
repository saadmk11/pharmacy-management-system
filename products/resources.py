from import_export import resources

from .models import Product


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        widgets = {
            'created_at': {'format': '%d-%m-%Y'},
            'updated_at': {'format': '%d-%m-%Y'}
        }
        fields = (
            'id',
            'name',
            'price',
            'available_quantity',
            'sku_id',
            'is_available',
            'created_at',
            'updated_at',
        )
        export_order = fields
