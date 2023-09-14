from typing import Any

from django.db.models import F

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .models import (
    Customer,
    Deal,
    Gem,
)


class CustomerSerializer(serializers.ModelSerializer):
    """сереализатор для модели пользователя."""
    class Meta:
        model = Customer
        fields = (
            'username',
            'spent_money',
            'count_gems',
        )


class GemSerializer(serializers.ModelSerializer):
    """сереализатор для модели камня."""
    class Meta:
        model = Gem
        fields = (
            'name',
        )


class DealSerializer(serializers.ModelSerializer):
    """сереализатор для модели сделки."""
    deals: list = []

    customer = serializers.CharField(
        max_length=64,
    )
    item = serializers.CharField(
        max_length=64,
    )

    class Meta:
        model = Deal
        fields = (
            'customer',
            'item',
            'total',
            'quantity',
            'date',
        )

    @classmethod
    def create(cls, validated_data: Any) -> None:
        """ создание экземпляров моделей,
        вызывается serializer.save()"""
        validated_data['item'], is_new_gem = (
            Gem
            .objects
            .get_or_create(
                name=validated_data['item'],
            )
        )

        validated_data['customer'], is_new_customer = (
            Customer
            .objects
            .get_or_create(
                username=validated_data['customer'],
            )
        )

        customer, gem = validated_data['customer'], validated_data['item']
        if gem not in customer.gems.all():
            customer.gems.add(gem)

        if is_new_customer:
            Customer.objects.filter(
                username=validated_data['customer'],
            ).update(spent_money=validated_data['total'])
        else:
            Customer.objects.filter(
                username=validated_data['customer'],
            ).update(
                spent_money=F('spent_money') + validated_data['total'],
            )

        cls.deals.append(validated_data)

    @classmethod
    def create_many(cls) -> Response:
        """метод массового создания сделок."""
        Deal.objects.bulk_create(
            [
                Deal(
                    username=deal['customer'],
                    item=deal['item'],
                    total=deal['total'],
                    quantity=deal['quantity'],
                    date=deal['date'],
                )
                for deal in cls.deals
            ],
        )
        cls.deals = []
        return Response(
            {'Status': 'OK - файл был обработан без ошибок;'}, status=status.HTTP_201_CREATED,
        )
