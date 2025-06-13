from django.contrib import admin
from .models import Category, Product, BotUser, ProductColor, ProductImage

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(BotUser)
admin.site.register(ProductColor)
admin.site.register(ProductImage)