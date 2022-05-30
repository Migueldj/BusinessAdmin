from rest_framework import routers, serializers, viewsets
from rest_framework.serializers import ModelSerializer

from .models import Product

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'