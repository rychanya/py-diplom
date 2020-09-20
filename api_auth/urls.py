from django.urls import path

from .views import (
    ConfirmResetPasword,
    LoginView,
    LogoutView,
    RegisterUserView,
    ResetPasswordView,
)

urlpatterns = [
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path("siginup", RegisterUserView.as_view()),
    path("reset_password", ResetPasswordView.as_view()),
    path(
        "reset_password/<str:uidb64>/<str:token>",
        ConfirmResetPasword.as_view(),
        name="password_reset_confirm",
    ),
]
