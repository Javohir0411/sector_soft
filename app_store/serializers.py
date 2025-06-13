from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from typing_extensions import ReadOnly

from app_store.models import (
    Category,
    Product,
    ProductColor,
    ProductImage
)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryGetSerializer(ModelSerializer):
    category_name = SerializerMethodField(method_name="get_category_name", read_only=True)
    subcategories = SerializerMethodField(method_name="get_subcategories", read_only=True)

    class Meta:
        model = Category
        fields = ('id', "category_name", "subcategories")

    def get_category_name(self, obj):
        lang = self.context.get('lang', 'uz')  # Default uz
        return obj.category_name_ru if lang == 'ru' else obj.category_name_uz

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        lang = self.context.get('lang', 'uz')

        return [
            {
                'id': sub.id,
                'category_name': sub.category_name_ru if lang == 'ru' else sub.category_name_uz
            }
            for sub in subcategories
        ]


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'color', 'image']




class ProductColorSerializer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductColor
        fields = ['id', 'product_color_uz', 'product_color_ru', 'price', 'currency', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        color = ProductColor.objects.create(**validated_data)
        for image_data in images_data:
            ProductImage.objects.create(color=color, **image_data)
        return color

class ProductGetSerializer(ModelSerializer):
    product_name = SerializerMethodField()
    product_description = SerializerMethodField()
    colors = ProductColorSerializer(many=True, read_only=True)
    categories = CategoryGetSerializer(source='product_categories', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', "product_name", "product_description", 'colors', 'categories')

    def get_product_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return obj.product_name_ru if lang == 'ru' else obj.product_name_uz

    def get_product_description(self, obj):
        lang = self.context.get('lang', 'uz')
        return obj.product_descriptions_ru if lang == 'ru' else obj.product_descriptions_uz



class ProductSerializer(ModelSerializer):
    colors = ProductColorSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name_uz', 'product_name_ru',
            'product_categories',
            'product_descriptions_uz', 'product_descriptions_ru',
            'colors'
        ]

    def create(self, validated_data):
        colors_data = validated_data.pop('colors', [])
        categories = validated_data.pop('product_categories', [])
        product = Product.objects.create(**validated_data)
        product.product_categories.set(categories)

        for color_data in colors_data:
            images_data = color_data.pop('images', [])
            color = ProductColor.objects.create(product=product, **color_data)
            for image_data in images_data:
                ProductImage.objects.create(color=color, **image_data)

        return product


"""
{
  "product_name_uz": "iPhone 14",
  "product_name_ru": "Айфон 14",
  "product_category": 1,
  "product_descriptions_uz": "Yangi iPhone",
  "product_descriptions_ru": "Новый Айфон",
  "colors": [
    {
      "product_color_uz": "Qora",
      "product_color_ru": "Черный",
      "price": "12000000.00",
      "currency": "UZS",
      "images": [
        {"image": "image1.jpg"},
        {"image": "image2.jpg"}
      ]
    }
  ]
}

"""
