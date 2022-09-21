from decimal import Decimal
from rest_framework import serializers
from .models import *

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'discounted_price', 'percentage_discount', 'product_description', 'categories']

    percentage_discount = serializers.SerializerMethodField(method_name='percentage_discount_')
    def percentage_discount_(self, product : Product):
        difference = product.product_price - product.discounted_price
        return (difference/product.product_price) * 100


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'unit_price', 'total_price']

    total_price = serializers.SerializerMethodField(method_name='total_price_')
    def total_price_(self, orderitem : OrderItem):
        return Decimal(orderitem.quantity) * orderitem.unit_price