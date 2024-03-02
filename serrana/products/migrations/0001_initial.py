# Generated by Django 5.0.2 on 2024-02-10 14:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_diameter', models.CharField(max_length=255)),
                ('product_weight', models.CharField(max_length=255)),
                ('storage_location', models.CharField(max_length=255, unique=True)),
                ('product_quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('min_stock_quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('max_stock_quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('product_status', models.CharField(max_length=255)),
            ],
        ),
    ]