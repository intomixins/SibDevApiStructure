from django.contrib import admin

from .models import (
    Customer,
    Deal,
    Gem,
)

admin.site.register(Customer)  # админка покупателя
admin.site.register(Gem)  # админка камня
admin.site.register(Deal)  # админка сделки
