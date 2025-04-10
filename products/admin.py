from django.contrib import admin
from .models import Product, Category, OrderItem, Order

admin.site.register(Product)
admin.site.register(Category)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  # Display user and created_at fields
    inlines = [OrderItemInline]  # Include the OrderItem inline
