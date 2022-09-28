from dataclasses import field
from decimal import Decimal
from pyexpat import model
from rest_framework import serializers
from .models import *

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_name']


class ProductSerializer(serializers.ModelSerializer):
    percentage_discount = serializers.SerializerMethodField()

    def get_percentage_discount(self, product : Product):
        difference = product.product_price - product.discounted_price
        percent =  (difference/product.product_price) * 100
        if percent < 0:
            return "No discount"
        return percent
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_price', 'discounted_price', 'percentage_discount', 'product_description', 'categories']


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_description','discounted_price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, orderitem : OrderItem):
        return Decimal(orderitem.quantity) * orderitem.product.discounted_price

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price_of_orders = serializers.SerializerMethodField()

    def get_total_price_of_orders(self, order_items : OrderItem):
        return sum([item.quantity * item.product.discounted_price for item in order_items.order_items.all()])


    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'order_items', 'total_price_of_orders']



class AddOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        order_id = self.context['order_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try: 
            order_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
            order_item.quantity += quantity
            order_item.save()
            self.instance = order_item
            
        except OrderItem.DoesNotExist:
            self.instance = OrderItem.objects.create(order_id=order_id, **self.validated_data)
        
        return self.instance

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity']


class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']
