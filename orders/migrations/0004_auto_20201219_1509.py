# Generated by Django 3.1 on 2020-12-19 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Confirmed'), (3, 'Cancelled')], default=1),
        ),
    ]
