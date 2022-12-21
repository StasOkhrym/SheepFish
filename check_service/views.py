from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action

from check_service.models import Printer, Check
from check_service.renderers import PDFRenderer
from check_service.serializers import (
    PrinterSerializer,
    CheckSerializer,
)
from sheep_fish.celery import app


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = CheckSerializer(data=data)
        if serializer.is_valid():
            check_data = serializer.validated_data
            checks = Check.objects.all()
            for check in checks:
                if (
                    check_data["order"]["order_number"]
                    == check.order.order_number
                ):
                    return JsonResponse(
                        {"order": "such order already exists"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            printer = check_data["printer"]
            point_id = printer.point_id
            if Printer.objects.filter(point_id=point_id).exists():
                self.perform_create(serializer)
                return JsonResponse(
                    {"check": "Check was created"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return JsonResponse(
                    {"printer": "There are no printers at mentioned point"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return JsonResponse(
                {"error": "Check data is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        serializer.save()
        check = self.get_object()
        printers = Printer.objects.filter(point_id=check.printer.point_id)
        for printer in printers:
            if printer.check_type == "kitchen":
                app.send_task(
                    "check_service.tasks.render_pdf_client",
                    (check, settings.KITCHEN_CHECK_TEMPLATE),
                )
            if printer.check_type == "client":
                app.send_task(
                    "check_service.tasks.render_pdf_client",
                    (check, settings.CLIENT_CHECK_TEMPLATE),
                )

    @action(methods=["get"], detail=True, renderer_classes=(PDFRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.pdf_file.open()
        response = FileResponse(file_handle, content_type="application/pdf")
        response["Content-Length"] = instance.file.size
        response["Content-Disposition"] = (
            'attachment; filename="%s"' % instance.file.name
        )
        if response.status_code == 200:
            instance.status = "printed"
            instance.save()
        return response
