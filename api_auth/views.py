from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.context_processors import request
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .mailing import send_reset_mail
from .serializers import (
    ConfirmResetPasswordSerializer,
    LoginSerializer,
    ResetPaswordSerializer,
    UserSerializer,
)


class RegisterUserView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("OK", status=status.HTTP_201_CREATED, headers=headers)


class ResetPasswordView(APIView):
    def get(self, request, format=None):
        serializer = ResetPaswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User = get_user_model()
        try:
            user = User.objects.get(email=serializer.data["email"])
            current_site = get_current_site(request)
            send_reset_mail(user, current_site)
        except User.DoesNotExist:
            pass
        return Response("ok")


class ConfirmResetPasword(APIView):
    def get(self, request, uidb64, token, format=None):
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(serializer.data["password1"])
            user.save()
        else:
            return Response("false")
        return Response("ok")


class LoginView(APIView):
    def get(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.data["email"], password=serializer.data["password"]
        )
        if user is not None:
            login(request, user)
            return Response("login")
        return Response("error")


class LogoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response("logout")
