from django.urls import path
from .views import product_list, order_product, remove_from_basket, view_basket, home
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', product_list, name='product_list'),
    path('order/', order_product, name='order_product'),
    path('view_basket/', view_basket, name='view_basket'),
    path('remove_from_basket/<int:product_id>/<str:size>/', remove_from_basket, name='remove_from_basket'),
    path('', home, name='home'),
    path('view_basket/', view_basket, name='view_basket'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

#Might not need this