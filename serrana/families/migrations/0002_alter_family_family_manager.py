# Generated by Django 5.0.2 on 2024-04-18 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='family_manager',
            field=models.CharField(max_length=255),
        ),
    ]