from django.contrib.auth.tokens import default_token_generator
from django.template.context_processors import request
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, permissions, serializers, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_yaml.parsers import YAMLParser

from .mailing import send_reset_mail
from .models import Cart, CartItem, Order, OrderItem, Product, Shop, User
from .serializers.auth import ConfirmResetPasswordSerializer, ResetPaswordSerializer
from .serializers.ordering import CartItemSerializer, CartSerializer, OrderSerializer
from .serializers.product import ProductSerializer
from .serializers.update import (
    CategoriesSerializer,
    ProductFileSerializer,
    UserSerializer,
)


class IsShopOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            name = request.data["shop"]
        except KeyError:
            return False
        try:
            shop = Shop.objects.get(name=name)
            return shop.owner == request.user
        except Shop.DoesNotExist:
            return True


class FileUploadView(APIView):
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
        product_serilizer = ProductFileSerializer(
            data=request.data.get("goods"), many=True
        )
        product_serilizer.is_valid(raise_exception=True)
        product_serilizer.save(shop=shop)
        return Response("ok")


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response("OK", status=status.HTTP_201_CREATED, headers=headers)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartAddView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartView(APIView):
    def get(self, request, format=None):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        goods_price = 0
        shops = {}
        for item in cart.cartitem_set.all():
            goods_price += item.price * item.quantity
            shops[item.product.shop.name] = item.product.shop.delivery_price
        shops_all = sum(shops.values())
        total_price = goods_price + shops_all
        serializer = CartSerializer(instance=cart)
        return Response(
            dict(
                serializer.data,
                goods_total=goods_price,
                shops=shops,
                total_price=total_price,
            )
        )


class PurchaseView(APIView):
    def get(self, request, format=None):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response("Корзина пуста")
        items = cart.cartitem_set.all()
        if not items:
            return Response("Корзина пуста")
        order = Order.objects.create(user=request.user)
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.price,
                quantity=item.quantity,
            )
        cart.delete()
        return Response(order.id)


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class ResetPasswordView(APIView):
    def get(self, request, format=None):
        serializer = ResetPaswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        try:
            user = User.objects.get(email=serializer.data["email"])
            send_reset_mail(user)
        except User.DoesNotExist:
            pass
        return Response("ok")


class ConfirmResetPasword(APIView):
    def get(self, request, uidb64, token, format=None):
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
