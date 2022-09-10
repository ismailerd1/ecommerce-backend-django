from unicodedata import category
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=255)


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField()
    slug = models.SlugField()
    product_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    product_description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


class Cart(models.Model):
    added_at = models.DateTimeField()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.BigIntegerField()


