from rest_framework import exceptions, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_yaml.parsers import YAMLParser

from .models import Shop
from .serializers import CategoriesSerializer, ProductSerializer


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            shop = Shop.objects.get(name=request.data["shop"])
            return shop.owner == request.user
        except Shop.DoesNotExist:
            return True


class ResetTokenView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        token = Token.objects.get(user=request.user)
        token.delete()
        token = Token.objects.create(user=request.user)
        return Response({"token": str(token)})


class FileUploadView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [permissions.IsAuthenticated, IsShopOwner]
    parser_classes = [
        YAMLParser,
    ]

    def post(self, request, format=None):
        shop, _ = Shop.objects.get_or_create(
            name=request.data["shop"], defaults={"owner": request.user}
        )
        category_serialyzer = CategoriesSerializer(
            data=request.data.get("categories"), many=True
        )
        category_serialyzer.is_valid(raise_exception=True)
        category_serialyzer.save()
        for good in request.data.get("goods"):
            good["parameters"] = [
                {"name": name, "value": value}
                for name, value in good["parameters"].items()
            ]
        product_serilizer = ProductSerializer(data=request.data.get("goods"), many=True)
        product_serilizer.is_valid(raise_exception=True)
        product_serilizer.save(shop=shop)
        return Response("ok")
