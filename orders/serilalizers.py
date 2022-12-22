from django.db.migrations import serializer
from rest_framework import serializers

from orders.models import Item, Order


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            "id",
            "quantity",
            "price",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "order_number",
            "items",
        )
