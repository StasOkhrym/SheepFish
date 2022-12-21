from django.contrib import admin
from check_service.models import Check, Printer


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    pass


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ("printer", "type", "status")
