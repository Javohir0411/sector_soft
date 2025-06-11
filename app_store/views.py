from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from app_store.models import Category, Product
from app_store.serializers import CategoryGetSerializer, CategorySerializer, ProductGetSerializer, ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategoryGetSerializer
        return CategorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["lang"] = self.request.query_params.get("lang", "uz")
        return context


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductGetSerializer
        return ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["lang"] = self.request.query_params.get("lang", "uz")
        return context