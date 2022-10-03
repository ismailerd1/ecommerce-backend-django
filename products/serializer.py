from decimal import Decimal
from django.db import transaction
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
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_price_of_orders = serializers.SerializerMethodField()

    def get_total_price_of_orders(self, order_items : OrderItem):
        return sum([item.quantity * item.product.discounted_price for item in order_items.order_items.all()])


    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at' ,'payment_status', 'order_items', 'total_price_of_orders']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']

            customer = Customer.objects.get_or_create(customer_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [OrderItem( order=order, product=item.product, discounted_price=item.product.discounted_price, quantity=item.quantity, total_price=item.total_price) for item in cart_items]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
