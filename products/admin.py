from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['category_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)