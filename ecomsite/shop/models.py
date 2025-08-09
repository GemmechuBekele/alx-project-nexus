from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Order(models.Model):
    name = models.CharField(max_length=2000)
    email = models.CharField(max_length=2000)
    address = models.CharField(max_length=2000)
    city = models.CharField(max_length=2000)
    state = models.CharField(max_length=2000)
    zipcode = models.CharField(max_length=1000)
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} — {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # price at purchase time

    def __str__(self):
        return f"{self.quantity} × {self.product.title} (Order {self.order.id})"
