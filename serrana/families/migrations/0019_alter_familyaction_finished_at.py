# Generated by Django 5.0.2 on 2024-04-25 23:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0018_alter_familyaction_finished_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familyaction',
            name='finished_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
