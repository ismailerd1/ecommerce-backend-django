from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from products.permissions import IsAdminOrReadOnly
from products.serializer import CategoriesSerializer, ProductSerializer, CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CartItemSerializer, CreateOrderSerializer, OrderSerializer, UpdateOrderSerializer
from products.models import Categories, Product, Cart, CartItem, Order, Customer

from django.db import transaction
from rest_framework import status
from django.core.cache import cache
from products.tasks import send_order_confirmation_email

class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        cached_products = cache.get('all_products')
        if cached_products is not None:
            return Response(cached_products)
        
        response = super().list(request, *args, **kwargs)
        cache.set('all_products', response.data, timeout=60*60) 
        return response

class CartViewSet(CreateModelMixin, RetrieveModelMixin , DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = CreateOrderSerializer(
                    data=request.data,
                    context={'user_id': self.request.user.id}
                )
                serializer.is_valid(raise_exception=True)
                order = serializer.save()  
                order_serializer = OrderSerializer(order)
                send_order_confirmation_email.delay(
                    order.id, 
                    self.request.user.email, 
                    self.request.user.first_name
                )
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        (customer_id, _) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)
