from django.contrib.auth import get_user_model
from django.db import models


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True
        db_table = "abstract_model"


class Category(AbstractBaseModel):
    category_name_uz = models.CharField(max_length=255)
    category_name_ru = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category_name_uz} | {self.category_name_ru}"

    class Meta:
        verbose_name_plural = "Categories"
        db_table = "categories"


class CurrencyChoice(models.TextChoices):
    UZS = "UZS", "So'm"
    USD = "USD", "Dollar"
    RUB = "RUB", "Rubl"


class Product(AbstractBaseModel):
    product_name_uz = models.CharField(max_length=255)
    product_name_ru = models.CharField(max_length=255)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to="product_images/")
    product_price = models.DecimalField(max_digits=15, decimal_places=2)
    product_price_currency = models.CharField(max_length=3, choices=CurrencyChoice, default=CurrencyChoice.UZS)
    product_descriptions_uz = models.TextField()
    product_descriptions_ru = models.TextField()

    def __str__(self):
        return f"{self.product_name_uz} | {self.product_price}"

    class Meta:
        verbose_name_plural = "Products"
        db_table = "Products"
