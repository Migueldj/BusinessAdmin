from django.forms import ValidationError
from rest_framework import routers, serializers, viewsets
from rest_framework.serializers import ModelSerializer

from .models import Product, Sale

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, value):
        if self.context.get('is_create'):
            product = Product.objects.filter(id = value['bar_code'])
            if not product.exists():
                raise serializers.ValidationError("Este código de barras ya existe")
        return value

class SaleSerializer(ModelSerializer):
    products = serializers.ListField()
    class Meta:
        model = Sale
        fields = "__all__"