from urllib import request
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializer import *
from .models import * 


class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class OrderViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin ,GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddOrderItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderItemSerializer
        return OrderItemSerializer

    def get_serializer_context(self):
        return {'order_id': self.kwargs['order_pk']}

    def get_queryset(self):
        return OrderItem.objects.filter(order_id=self.kwargs['order_pk']).select_related('product')