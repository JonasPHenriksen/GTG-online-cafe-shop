"""
URL configuration for cafe_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from products.views import home, add_to_basket, view_basket, place_order, bypass_login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('add_to_basket/<int:product_id>/', add_to_basket, name='add_to_basket'),  
    path('basket/', view_basket, name='basket'),
    path('place_order/', place_order, name='place_order'),
    path('', home, name='home'),
    path('view_basket/', view_basket, name='view_basket'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('bypass-login/', bypass_login, name='bypass_login'),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
