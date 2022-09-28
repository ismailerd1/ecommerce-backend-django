from pyexpat import model
from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username','email', 'phone']


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Customer
        fields = ['first_name', 'last_name', 'username']