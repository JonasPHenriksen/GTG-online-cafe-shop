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
    user = models.CharField(max_length=150)  # Store the username as a string
    name = models.CharField(max_length=200)  # Name of the person placing the order
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the order was created
    status = models.CharField(max_length=20, default='in_progress')  # Add a status field (default 'in_progress')

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Link to the Order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the Product
    quantity = models.PositiveIntegerField(default=1)  # Store the quantity of the product

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"

class BasketItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"