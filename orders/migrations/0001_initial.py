# Generated by Django 3.1 on 2020-12-18 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=128)),
                ('contact_no', models.CharField(max_length=11)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('payment_status', models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Cancelled')], default=1)),
                ('order_status', models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Confirmed'), (6, 'Cancelled')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='products.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
