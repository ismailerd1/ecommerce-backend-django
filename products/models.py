from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import MinValueValidator

from accounts.models import Customer


class Categories(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.category_name
    class Meta:
        indexes = [
            models.Index(fields=['category_name']),  
        ]

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(null=True, blank=True, upload_to='products/images')
    slug = models.SlugField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    product_description = models.TextField()
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product_name

    class Meta:
        ordering = ['product_name', 'product_price']
        indexes = [
            models.Index(fields=['product_name']),  
            models.Index(fields=['product_price']),
            models.Index(fields=['categories']),
        ]


class Cart(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['added_at']),  
        ]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.BigIntegerField()

    def __str__(self) -> str:
        return self.product

class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, related_name='customer')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return self.customer.first_name
    class Meta:
        indexes = [
            models.Index(fields=['placed_at']),  
            models.Index(fields=['payment_status']), 
        ]
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.quantity
    class Meta:
        indexes = [
            models.Index(fields=['order']), 
            models.Index(fields=['product']),
        ]
