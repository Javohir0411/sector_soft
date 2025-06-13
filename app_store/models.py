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
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories"
    )
    objects = models.Manager
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
    product_categories = models.ManyToManyField(Category, related_name="products")
    product_image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    product_descriptions_uz = models.TextField()
    product_descriptions_ru = models.TextField()

    def __str__(self):
        return f"{self.product_name_uz} | {self.product_name_ru}"

    class Meta:
        verbose_name_plural = "Products"
        db_table = "Products"


class ProductColor(AbstractBaseModel):  # har xil mahsulot, har xil rangda va rangiga qarab, boshqacha narxda
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    product_color_uz = models.CharField(max_length=200)
    product_color_ru = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CurrencyChoice, default=CurrencyChoice.UZS)



    def __str__(self):
        return f"{self.product} | {self.product_color_uz}"

    class Meta:
        verbose_name_plural = "ProductColors"
        db_table = "ProductColor"


class ProductImage(AbstractBaseModel):
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"{self.color} | {self.image}"

    class Meta:
        verbose_name_plural = "ProductImages"
        db_table = "ProductImage"


class BotUser(AbstractBaseModel):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    lang = models.CharField(max_length=2, choices=[("uz", "Uzbek"), ("ru", "Russian")], default="uz")

    objects = models.Manager

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "BotUsers"
        db_table = "BotUser"
