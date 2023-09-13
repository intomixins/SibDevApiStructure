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
    def top_five_total(cls) -> QuerySet:
        return Customer.objects.prefetch_related('gems').order_by('spent_money')

    @classmethod
    def import_csv(cls, file_object: Any) -> Response:
        reader = csv.DictReader(codecs.iterdecode(file_object, 'utf-8'), delimiter=',')
        serializer = DealSerializer(data=list(reader), many=True)
        if serializer.is_valid():
            serializer.save()
            DealSerializer.create_many()
        return Response({
            'data': serializer.errors,
        })
