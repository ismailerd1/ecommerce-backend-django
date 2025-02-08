from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import Customer
from accounts.serializers import CustomerSerializer

from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @ratelimit(key='ip', rate='15/m', method='ALL')
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        cache_key = f'customer_{request.user.id}'  

        cached_customer = cache.get(cache_key)
        if cached_customer is not None:
            return Response(cached_customer)

        (customer, _) = Customer.objects.get_or_create(user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            data = serializer.data
            cache.set(cache_key, data, timeout=60*30) 
            return Response(data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raiseExceptions=True)
            serializer.save()
            cache.set(cache_key, serializer.data, timeout=10*60)
            return Response(serializer.data)
