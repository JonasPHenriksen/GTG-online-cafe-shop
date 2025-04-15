from django.urls import path
from .views import product_list, order_product, remove_from_basket

urlpatterns = [
    path('', product_list, name='product_list'),
    path('order/', order_product, name='order_product'),
    path('remove_from_basket/<int:product_id>/', remove_from_basket, name='remove_from_basket'),
]
