from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import serializers

from .mailing import send_confirm_mail


class UserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField()
    first_name = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = [
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "password",
            "company",
            "position",
        ]

    extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model()(
            email=validated_data["email"],
            username=validated_data["email"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            middle_name=validated_data["middle_name"],
            company=validated_data["company"],
            position=validated_data["position"],
            is_active=False,
        )
        user.set_password(validated_data["password"])
        user.save()
        current_site = get_current_site(self.context["request"])
        send_confirm_mail(user, current_site)
        return user


class ResetPaswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data["password1"] != data["password2"]:
            return serializers.ValidationError("password incorect")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
