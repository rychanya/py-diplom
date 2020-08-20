from django.urls import path
from rest_framework.authtoken import views

from .views import FileUploadView, ResetTokenView

urlpatterns = [
    path("token/get", views.obtain_auth_token),
    path("token/reset", ResetTokenView.as_view()),
    path("upload", FileUploadView.as_view()),
]
