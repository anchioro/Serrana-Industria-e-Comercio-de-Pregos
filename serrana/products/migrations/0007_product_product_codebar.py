# Generated by Django 5.0.2 on 2024-02-14 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_codebar',
            field=models.CharField(default=8904306000080, max_length=13),
            preserve_default=False,
        ),
    ]
