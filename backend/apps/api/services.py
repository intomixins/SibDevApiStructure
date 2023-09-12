import csv
from typing import Any

from django.db.models import QuerySet

from .models import Customer


def top_five_total() -> QuerySet:
    return Customer.objects.order_by('spent_money').prefetch_related('gems')


def import_csv(csv_file: Any) -> Any:
    reader = csv.DictReader(
        (line.decode() for line in csv_file),
        fieldnames=[
            'username',
            'item',
            'total',
            'quantity',
            'date',
        ],
    )

    deals = []
    next(reader)
    for row in reader:
        deals.append(row)

    return (deals, type(deals))
