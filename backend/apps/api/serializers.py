from rest_framework import serializers

from .models import (
    Customer,
    # Deal,
    Gem,
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'username',
            'spent_money',
            'gems',
        )


class GemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gem
        fields = (
            'name',
        )
