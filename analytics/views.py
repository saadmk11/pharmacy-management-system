from django.contrib.auth.mixins import AccessMixin
from django.db.models import (
    DecimalField,
    Count,
    When,
    IntegerField,
    Case,
    Sum,
    F,
    Q,
)
from django.db.models.functions import TruncMonth, Coalesce
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from orders.constants import ORDER_PENDING, ORDER_CONFIRMED, ORDER_CANCELED, PAYMENT_CONFIRMED
from orders.models import Order, OrderItem
from products.models import Product


class AdminRequiredMixin(AccessMixin):
    login_url = reverse_lazy('admin:login')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the current user is authenticated and is admin."""
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AnalyticsView(AdminRequiredMixin, TemplateView):
    template_name = 'analytics/analytics_dashboard.html'

    def get_analytics_data(self):
        total_order_count = Order.objects.all().aggregate(
            pending_order_count=Count(Case(
                When(order_status=ORDER_PENDING, then=1),
                output_field=IntegerField(),
            )),
            confirmed_order_count=Count(Case(
                When(order_status=ORDER_CONFIRMED, then=1),
                output_field=IntegerField(),
            )),
            canceled_order_count=Count(Case(
                When(order_status=ORDER_CANCELED, then=1),
                output_field=IntegerField(),
            )),
            unique_order_count=Count('contact_no', distinct=True),
            all_order_count=Count('id')
        )

        total_revenue_without_discount = (OrderItem.objects.filter(
            order__order_status=ORDER_CONFIRMED,
            order__payment_status=PAYMENT_CONFIRMED
        ).aggregate(
            total_revenue=Sum(
                F('price') * F('quantity'), output_field=DecimalField()
            )
        )['total_revenue']) or 0.0

        total_discount = (Order.objects.filter(
            order_status=ORDER_CONFIRMED,
            payment_status=PAYMENT_CONFIRMED
        ).aggregate(
            total_discount=Sum(
                F('discount'), output_field=DecimalField()
            )
        )['total_discount']) or 0.0

        total_revenue = total_revenue_without_discount - total_discount

        order_queryset = Order.objects.annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id'),
        ).order_by('-month')[:12]

        order_labels = []
        order_data = []

        for item in order_queryset:
            month_year = '{} ({})'.format(
                item['month'].strftime('%b'),
                item['month'].year
            )
            order_labels.append(month_year)
            order_data.append(item['count'])

        revenue_queryset = OrderItem.objects.filter(
            order__order_status=ORDER_CONFIRMED,
            order__payment_status=PAYMENT_CONFIRMED
        ).annotate(
            month=TruncMonth('order__created_at')
        ).values('month').annotate(
            sum=Sum(
                F('price') * F('quantity'), output_field=DecimalField()
            ),
        ).order_by('-month')[:12]

        order_revenue_labels = []
        order_revenue_data = []

        for item in revenue_queryset:
            month_year = '{} ({})'.format(
                item['month'].strftime('%b'),
                item['month'].year
            )
            order_revenue_labels.append(month_year)
            order_revenue_data.append((str(item['sum'])))

        products_sold_count = Product.objects.annotate(
            sold_count=Coalesce(
                Sum(
                    'order_items__quantity',
                    output_field=IntegerField(),
                    filter=Q(
                        order_items__order__isnull=False,
                        order_items__order__order_status=ORDER_CONFIRMED,
                        order_items__order__payment_status=PAYMENT_CONFIRMED
                    )
                ), 0
            )
        )

        most_sold_products = products_sold_count.order_by(
            '-sold_count'
        ).values('name', 'price', 'sku_id', 'sold_count')[:10]

        data = {
            'most_sold_products': most_sold_products,
            'order_revenue_labels': order_revenue_labels,
            'order_revenue_data': order_revenue_data,
            'order_labels': order_labels,
            'order_data': order_data,
            'total_revenue': total_revenue,
            'total_order_count': total_order_count,
        }

        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.get_analytics_data()
        return context
