from api.models import BaseProduct, Category, Parameter, Product, ProductParameter, Shop
from rest_framework import serializers


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class ProductParameterSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="parameter.name")

    class Meta:
        model = ProductParameter
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    parameters = ProductParameterSerializer(
        many=True, read_only=True, source="productparameter_set"
    )
    category = serializers.ReadOnlyField(source="base.category.name")
    name = serializers.ReadOnlyField(source="base.name")
    shop = ShopSerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "model",
            "name",
            "price_rrc",
            "quantity",
            "parameters",
            "shop",
        ]
