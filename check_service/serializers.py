from rest_framework import serializers

from check_service.models import Printer, Check


class PrinterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = (
            "id",
            "name",
            "check_type",
            "point_id",
        )


class ItemSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class OrderSerializer(serializers.Serializer):
    order_number = serializers.IntegerField()
    items = ItemSerializer(many=True, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


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
