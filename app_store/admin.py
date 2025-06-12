from django.contrib import admin
from .models import Product, ProductColor, ProductImage, Category, BotUser


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Nechta bo'sh forma ko'rsatilsin

class ProductColorInline(admin.StackedInline):  # yoki admin.TabularInline
    model = ProductColor
    extra = 1
    inlines = [ProductImageInline]  # optional: agar rasmni ham ichida ko'rsatmoqchi bo'lsangiz

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "full_name", "phone_number", "created_at")
    search_fields = ("full_name", "phone_number", "telegram_id")
    list_filter = ("created_at",)
    ordering = ("-created_at",)








"""
from django.contrib import admin
from .models import Product, ProductColor, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductColorInline(admin.StackedInline):
    model = ProductColor
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorInline, ProductImageInline]  # ikkala inline alohida


admin.site.register(Product, ProductAdmin)
"""