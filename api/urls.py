from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CartAddView,
    CartView,
    FileUploadView,
    OrderViewSet,
    ProductListView,
    PurchaseView,
    RegisterUserView,
)

urlpatterns = [
    path("upload", FileUploadView.as_view()),
    path("register", RegisterUserView.as_view()),
    path("list", ProductListView.as_view()),
    path("cart/add", CartAddView.as_view()),
    path("cart", CartView.as_view()),
    path("purchase", PurchaseView.as_view()),
]

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")

urlpatterns = urlpatterns + router.urls
