# Generated by Django 3.1 on 2020-12-18 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
