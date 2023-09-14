import codecs
import csv
from typing import Any

from django.db.models import (
    QuerySet,
)

from rest_framework.response import Response

from .models import (
    Customer,
)
from .serializers import DealSerializer


class CustomerService:
    @classmethod
    def final_result(cls) -> QuerySet:
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
        return top_five

    @classmethod
    def import_csv(cls, file_object: Any) -> Response:
        """импортиррование csv файла."""
        reader = csv.DictReader(codecs.iterdecode(file_object, 'utf-8'), delimiter=',')
        serializer = DealSerializer(data=list(reader), many=True)
        if serializer.is_valid():
            serializer.save()
            return DealSerializer.create_many()
        return Response({
            'data': f'Error, Desc: {serializer.error_messages}'
                    '- в процессе обработки файла произошли ошибки.',
        })
