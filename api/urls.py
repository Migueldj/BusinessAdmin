from django.urls import path, include

from . import views

urlpatterns=[
   #Test
   path('test/', views.test),
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