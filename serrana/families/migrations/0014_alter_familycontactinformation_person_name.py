# Generated by Django 5.0.2 on 2024-04-24 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0013_alter_familycontactinformation_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familycontactinformation',
            name='person_name',
            field=models.CharField(max_length=255),
        ),
    ]
