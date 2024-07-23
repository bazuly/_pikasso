from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


# В рамках тестового задания будем использовать
# встроенную в джанго модель пользователя

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password"
        )


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeModel
        fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeRentalModel
        fields = '__all__'


class RentalReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeRentalModel
        fields = (
            'id',
            'user',
            'rental_start',
            'rental_end',
           #  'cost'
        )

    def get_cost(self, obj):
        return obj.calculate_rental_cost()


class BikeRentalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeRentalModel
        fields = (
            'id',
            'bike',
            'rental_start',
            'rental_end',
        )
