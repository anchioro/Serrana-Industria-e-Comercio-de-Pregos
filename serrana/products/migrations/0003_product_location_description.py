# Generated by Django 5.0.2 on 2024-02-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_options_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='location_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
