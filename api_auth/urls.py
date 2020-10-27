from django.urls import path

from .views import (
    ConfirmEmail,
    ConfirmResetPasword,
    LoginView,
    LogoutView,
    RegisterUserView,
    ResetPasswordView,
)

urlpatterns = [
    path("login", LoginView.as_view(), name="api-login"),
    path("logout", LogoutView.as_view(), name="api-logout"),
    path("registration", RegisterUserView.as_view(), name="api-registration"),
    path("reset_password", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "reset_password/<str:uidb64>/<str:token>",
        ConfirmResetPasword.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "confirm_email/<str:uidb64>/<str:token>",
        ConfirmEmail.as_view(),
        name="confirm_email",
    ),
]
