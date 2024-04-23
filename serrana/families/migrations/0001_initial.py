# Generated by Django 5.0.2 on 2024-04-17 23:43

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_manager', models.TextField()),
                ('slug', models.CharField(blank=True, max_length=255)),
                ('zip_code', models.CharField(max_length=8)),
                ('state', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=10)),
                ('address_description', models.TextField(blank=True, null=True)),
                ('last_delivery', models.DateTimeField()),
                ('last_payment', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Família',
                'verbose_name_plural': 'Famílias',
            },
        ),
        migrations.CreateModel(
            name='FamilyAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('rubber_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('metal_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('is_finished', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='families.family')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.stock')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyContactInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.TextField()),
                ('phone', models.CharField(max_length=11)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('is_valid_phone_for_payment', models.BooleanField(default=False)),
                ('is_valid_cpf_for_payment', models.BooleanField(default=False)),
                ('is_valid_email_for_payment', models.BooleanField(default=False)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='families.family')),
            ],
        ),
    ]