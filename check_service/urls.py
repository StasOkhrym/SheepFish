from django.urls import path, include
from check_service.views import PrinterViewSet, CheckViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("printers", PrinterViewSet)
router.register("checks", CheckViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "check_service"
