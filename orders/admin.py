from django.contrib import admin

from orders.models import Order, Item


admin.site.register(Item)
admin.site.register(Order)
