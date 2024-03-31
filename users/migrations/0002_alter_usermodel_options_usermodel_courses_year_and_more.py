# Generated by Django 5.0.3 on 2024-03-28 07:07

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodel',
            options={'ordering': ['username']},
        ),
        migrations.AddField(
            model_name='usermodel',
            name='courses_year',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='group_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_cook',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_grant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='last_logged_device',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='last_logged_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='last_time_eat',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='student_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='id',
            field=models.UUIDField(auto_created=True, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterModelTable(
            name='usermodel',
            table='users',
        ),
        migrations.CreateModel(
            name='OTPModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires_at', models.DateTimeField(auto_created=True, blank=True, default=datetime.datetime(2024, 3, 28, 7, 12, 15, 613686), editable=False, null=True)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
