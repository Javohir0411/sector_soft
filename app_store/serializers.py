from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from app_store.models import (
    Category,
    Product
)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryGetSerializer(ModelSerializer):
    category_name = SerializerMethodField(method_name="get_category_name", read_only=True)

    class Meta:
        model = Category
        fields = ('id', "category_name")

    def get_category_name(self, obj):
        lang = self.context.get('lang', 'uz')  # Default uz
        return obj.category_name_ru if lang == 'ru' else obj.category_name_uz

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class ProductGetSerializer(ModelSerializer):
    product_name = SerializerMethodField(method_name="get_product_name", read_only=True)
    product_description = SerializerMethodField(method_name="get_product_description", read_only=True)

    class Meta:
        model = Product
        fields = ('id', "product_name", "product_price")

    def get_product_name(self, obj):
        lang = self.context.get('lang', 'uz')
        return obj.product_name_ru if lang == 'ru' else obj.product_name_uz



