from django.urls import path, include

from . import views
urlpatterns=[
   path('get-products', views.getProducts),
   path('get-product/<int:pk>/', views.getProduct),
]