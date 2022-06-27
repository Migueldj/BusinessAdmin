from django.contrib import admin
from .models import Product, Sale, ProductSale, ProductInventory, InboundInventory, OutboundInventory
# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(ProductSale)
admin.site.register(ProductInventory)
admin.site.register(InboundInventory)
admin.site.register(OutboundInventory)