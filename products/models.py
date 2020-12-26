from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )
    available_quantity = models.PositiveIntegerField(null=True, blank=True)
    sku_id = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return f'{self.name} - {self.price} Tk.'
