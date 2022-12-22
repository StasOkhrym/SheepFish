from rest_framework import serializers

from check_service.models import Printer, Check
from orders.serilalizers import OrderSerializer


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = (
            "id",
            "name",
            "check_type",
            "point_id",
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
