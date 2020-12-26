from django.db import models
from django.db.models import Sum, F, DecimalField

from orders.constants import (
    PAYMENT_STATUS_CHOICES,
    PAYMENT_PENDING,
    ORDER_STATUS_CHOICES,
    ORDER_PENDING,
)
from products.models import Product


class Order(models.Model):
    customer_name = models.CharField(max_length=128)
    contact_no = models.CharField(max_length=11)
    discount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.00
    )
    payment_status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_PENDING,
    )
    order_status = models.PositiveSmallIntegerField(
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.customer_name

    @property
    def sub_total(self):
        sub_total = self.items.aggregate(
            price_sum=Sum(
                F('price') * F('quantity'), output_field=DecimalField()
            )
        )['price_sum']

        if sub_total:
            return round(sub_total, 1)
        return 0

    @property
    def total(self):
        if self.discount:
            return self.sub_total - self.discount

        return self.sub_total

    @property
    def total_quantity(self):
        total_quantity = self.items.aggregate(
            price_sum=Sum(F('quantity'))
        )['price_sum']

        return total_quantity or 0


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        max_digits=9, decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price if self.product else 0
        super().save(*args, **kwargs)

    @property
    def item_total(self):
        return round(self.price * self.quantity, 1)

    def __str__(self):
        return self.order.customer_name
