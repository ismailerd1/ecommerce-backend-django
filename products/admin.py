from itertools import product
from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['category_name']

class ProductFilter(admin.SimpleListFilter):
    title = 'product price'
    parameter_name = 'product_price'

    def lookups(self, request, model_admin) :
        return [
            ('<100', 'Less than 100'),
            ('>100 & <500', '101-500'),
            ('>500 & <2000', '501-2000'),
            ('>2000', 'greater than 2000')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<100':
            return queryset.filter(product_price__lt=100)

        if self.value() == '>100 & <500':
            return queryset.filter(product_price__gt=100, product_price__lt=500)
        
        if self.value() == '>500 & <2000':
            return queryset.filter(product_price__gt=500, product_price__lt=2000)

        if self.value() == '>2000':
            return queryset.filter(product_price__gt=2000)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name']
    autocomplete_fields = ['category']
    list_display = ['product_name', 'category', 'product_price']
    list_filter = ['category', ProductFilter]

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