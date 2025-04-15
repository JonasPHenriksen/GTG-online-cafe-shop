from django.contrib import admin
from .models import Product, Category, OrderItem, Order

admin.site.register(Product)
admin.site.register(Category)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # No extra empty forms

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')
    list_filter = ('status',)
    inlines = [OrderItemInline]

    # Optional: You can add search fields, ordering, etc.
    search_fields = ('user',)
    ordering = ('-created_at',)
