from django.urls import path
from rest_framework.authtoken import views
from .views import ResetTokenView

urlpatterns = [
    path('token/', views.obtain_auth_token),
    path('token/reset', ResetTokenView.as_view()),
]
