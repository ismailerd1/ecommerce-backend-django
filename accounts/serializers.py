from rest_framework import serializers

from accounts.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone']


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Customer
        fields = ['user_first_name', 'user_last_name', 'user_username']
