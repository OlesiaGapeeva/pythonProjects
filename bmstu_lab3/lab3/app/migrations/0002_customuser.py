# Generated by Django 4.2.4 on 2023-11-27 17:36

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email адрес')),
                ('password', models.CharField(max_length=150, verbose_name='Пароль')),
                ('full_name', models.CharField(default='', max_length=50, verbose_name='ФИО')),
                ('phone_number', models.CharField(default='', max_length=30, verbose_name='Номер телефона')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Является ли пользователь менеджером?')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Является ли пользователь админом?')),
                ('groups', models.ManyToManyField(related_name='custom_users', related_query_name='custom_user', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='custom_users', related_query_name='custom_user', to='auth.permission')),
            ],
            options={
                'managed': True,
            },
            managers=[
                ('objects', app.models.NewUserManager()),
            ],
        ),
    ]
