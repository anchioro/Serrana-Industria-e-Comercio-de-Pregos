# Generated by Django 5.0.2 on 2024-02-14 14:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
