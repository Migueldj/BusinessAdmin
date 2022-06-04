from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns=[
   #Products
   path('get-products/', views.getProducts),
   path('create-product/', views.createProduct),
   path('update-product/', views.updateProduct),
   #Sales
   path('create-sale/', views.createSale),
   #Inventory
   path('get-inventory/', views.getInventory),
   path('add-inventory/', views.addInventory),
]