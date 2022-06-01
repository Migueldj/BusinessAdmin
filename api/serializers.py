from itertools import product
from math import prod
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from .models import Product, ProductInventory, Sale

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate(self, value):
        if self.context.get('is_create'):
            product = Product.objects.filter(id = value['bar_code'])
            if not product.exists():
                raise ValidationError("This bar code is already associated to an existing product")
        return value

class CreateSaleSerializer(Serializer):
    products = serializers.CharField()
    pieces = serializers.CharField()

    def validate(self, value):
        products_list = value['products'].split(',')
        pieces_list = [int(item) for item in value["pieces"].split(',')]

        #Validating all products have number of pieces
        if len(products_list) != len(pieces_list):
            raise ValidationError("Not all pieces for all products are provided")

        #Creating a list with all the product instances
        #Also validating those products exist
        product_instances = []
        for idx, product_id in enumerate(products_list):
            qs_product = Product.objects.filter(id = product_id)
            if qs_product.exists():
                product_id_instance = qs_product.first()
                product_instances.append(product_id_instance)

                #Validating stock available
                qs_inventory = ProductInventory.objects.filter(product = product_id_instance)
                if qs_inventory.exists():
                    if not qs_inventory.first().stock > pieces_list[idx]:
                        raise ValidationError(f"Not enough stock for {product_id_instance.name} asking for {pieces_list[idx]} available {qs_inventory.first().stock}")
                else:
                    raise ValidationError(f"There is no stock for {product_id_instance.name}")
            else:
                raise ValidationError(f"Product with id {product_id} is not in the database")

