from django.urls import path, include
from .views import ItemViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("printers", ItemViewSet)
router.register("checks", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "orders"
