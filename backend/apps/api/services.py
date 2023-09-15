import codecs
import csv
import os
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import (
    QuerySet,
)

from rest_framework import status
from rest_framework.response import Response

from .models import (
    Customer,
)
from .serializers import DealSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class CustomerService:
    @classmethod
    def final_result(cls) -> QuerySet:
        customers_cache = cache.get('customers_cache')
        if not customers_cache:
            top_five = (
                Customer
                .objects
                .prefetch_related('gems')
                .order_by('-spent_money')[:5]
            )
            gems_dict: dict = {}
            gems_set: set = set()
            for customer in top_five:
                for gem in customer.gems.all():
                    if gem in gems_dict:
                        gems_dict[gem] += 1
                        gems_set.add(gem.name)
                    else:
                        gems_dict[gem] = 1
            for customer in top_five:
                for gem in customer.gems.all():
                    if gem.name in gems_set:
                        customer.count_gems += f'{gem.name}, '
                customer.count_gems = customer.count_gems[:-2]
            cache.set('customers_cache', top_five, CACHE_TTL)
            return top_five
        return customers_cache

    @classmethod
    def import_csv(cls, file_object: Any) -> Response:
        """импортирование csv файла."""
        if file_object is None:
            return Response({
                'Response': 'Пожалуйста, отправьте csv файл.'},
                status=status.HTTP_204_NO_CONTENT,
            )
        _, file_ext = os.path.splitext(file_object.name)
        if file_ext != '.csv':
            return Response({
                'Response': 'Вы отправили файл с неправильным расширением. Нужен csv.'},
                status=status.HTTP_205_RESET_CONTENT,
            )
        reader = csv.DictReader(codecs.iterdecode(file_object, 'utf-8'), delimiter=',')
        serializer = DealSerializer(data=list(reader), many=True)
        if serializer.is_valid():
            if serializer.validated_data == []:
                return Response({
                    'Response': 'Вы отправили пустой файл.'},
                    status=status.HTTP_204_NO_CONTENT,
                )
            serializer.save()
            return DealSerializer.create_many()
        return Response({
            'data': f'Error, Desc: {serializer.error_messages}'
                    '- в процессе обработки файла произошли ошибки.',
        })
