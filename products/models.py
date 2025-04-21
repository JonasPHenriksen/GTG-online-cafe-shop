from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, related_name='products')

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('DELIVERED', 'Delivered'),
        ('PAID', 'Paid'),
    ]

    PAYMENT_CHOICES = [
        ('VIACARD', 'ViaCard'),
        ('CREDITCARD', 'CreditCard'),
        ('MOBILEPAY', 'MobilePay'),
        ('NONE', 'None'),
    ]

    user = models.CharField(max_length=150)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='NONE')

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    size = models.CharField(max_length=50)  
    quantity = models.PositiveIntegerField(default=1)  

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"

class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"