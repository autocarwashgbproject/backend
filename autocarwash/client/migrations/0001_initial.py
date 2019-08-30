# Generated by Django 2.2.4 on 2019-08-30 03:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона необходимо вводить в формате: «+79031234567». Допускается до 14 цифр.', regex='^\\+?1?\\d{9,14}$')])),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('surname', models.CharField(blank=True, max_length=20, null=True)),
                ('patronymic', models.CharField(blank=True, max_length=20, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(null=True, verbose_name='День рождения')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('first_login', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('delete_date', models.DateTimeField(blank=True, null=True, verbose_name='Удален')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneOTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Номер телефона необходимо вводить в формате: «+79031234567». Допускается до 14 цифр.', regex='^\\+?1?\\d{9,14}$')])),
                ('otp', models.CharField(blank=True, max_length=9, null=True)),
                ('count', models.IntegerField(default=0, help_text='Количетсво отправленных кодов проверки')),
            ],
        ),
    ]
