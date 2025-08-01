# Generated by Django 5.2.3 on 2025-06-12 12:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0006_alter_product_product_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_price_currency',
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_color_uz', models.CharField(max_length=200)),
                ('product_color_ru', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('currency', models.CharField(choices=[('UZS', "So'm"), ('USD', 'Dollar'), ('RUB', 'Rubl')], default='UZS', max_length=3)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='app_store.product')),
            ],
            options={
                'verbose_name_plural': 'ProductColors',
                'db_table': 'ProductColor',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='product_images/')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_store.productcolor')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'ProductImages',
                'db_table': 'ProductImage',
            },
        ),
    ]
