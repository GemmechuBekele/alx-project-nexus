from rest_framework import serializers
from .models import Products, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id', 'title', 'price', 'discount_price',
            'category', 'description', 'image'
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'items', 'name', 'email',
            'address', 'city', 'state', 'zipcode', 'total'
        ]
