from django.urls import path
from .views import product_list, order_product

urlpatterns = [
    path('', product_list, name='product_list'),
    path('order/', order_product, name='order_product'),
]
