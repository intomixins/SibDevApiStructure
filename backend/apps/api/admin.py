from django.contrib import admin

from .models import (
    Customer,
    Gem,
)

admin.site.register(Customer)
admin.site.register(Gem)
