from rest_framework import serializers

from check_service.models import Printer, Check
from check_service.tasks import Order, Item


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = (
            "id",
            "check_type",
            "api_key",
            "check_type",
            "point_id",
        )


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = (
            "name",
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


class CheckSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False)

    class Meta:
        model = Check
        fields = (
            "id",
            "printer",
            "type",
            "order",
            "status",
            "pdf_file",
        )