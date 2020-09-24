from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    CartAddView,
    CartView,
    FileUploadView,
    OrderViewSet,
    ProductListView,
    PurchaseView,
)

urlpatterns = [
    path("upload", FileUploadView.as_view()),
    # path("register", RegisterUserView.as_view()),
    path("list", ProductListView.as_view()),
    path("cart/add", CartAddView.as_view()),
    path("cart", CartView.as_view()),
    path("purchase", PurchaseView.as_view()),
    # path("reset", ResetPasswordView.as_view()),
    # path(
    #     "confirm/<str:uidb64>/<str:token>",
    #     ConfirmResetPasword.as_view(),
    #     name="password_reset_confirm",
    # ),
]

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")

urlpatterns = urlpatterns + router.urls
