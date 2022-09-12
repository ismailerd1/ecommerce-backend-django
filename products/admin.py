from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['category_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name']
    autocomplete_fields = ['category']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['added_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['cart', 'product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order', 'product']