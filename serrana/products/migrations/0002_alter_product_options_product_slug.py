# Generated by Django 5.0.2 on 2024-02-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'produto', 'verbose_name_plural': 'produtos'},
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
