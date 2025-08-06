from django.db import models

# Create your models here.


class Products(models.Model):

    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=500)


class Order(models.Model):
    items = models.CharField(max_length=5000)
    name = models.CharField(max_length=2000)
    email = models.CharField(max_length=2000)
    address = models.CharField(max_length=2000)
    city = models.CharField(max_length=2000)
    state = models.CharField(max_length=2000)
    zipcode = models.CharField(max_length=1000)
    total = models.FloatField()
