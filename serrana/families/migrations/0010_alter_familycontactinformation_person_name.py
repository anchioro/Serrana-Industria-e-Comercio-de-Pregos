# Generated by Django 5.0.2 on 2024-04-23 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0009_alter_familyaction_product_packing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familycontactinformation',
            name='person_name',
            field=models.CharField(max_length=255),
        ),
    ]
