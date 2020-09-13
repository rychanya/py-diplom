from rest_framework import serializers


class ResetPaswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, data):
        if data["password1"] != data["password2"]:
            return serializers.ValidationError("password incorect")
        return data
