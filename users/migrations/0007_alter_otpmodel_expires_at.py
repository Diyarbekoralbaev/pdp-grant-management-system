# Generated by Django 5.0.3 on 2024-03-29 07:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_otpmodel_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmodel',
            name='expires_at',
            field=models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime(2024, 3, 29, 7, 49, 46, 16390), editable=False, null=True),
        ),
    ]
