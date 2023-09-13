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
    gems = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        many=True,
    )

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


class DealSerializer(serializers.ModelSerializer):
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
        validated_data['item'] = (
            Gem
            .objects
            .get_or_create(
                name=validated_data['item'],
            )
        )[0]

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
            {'status': 'Imported'}, status=status.HTTP_201_CREATED,
        )
