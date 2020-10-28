from rest_framework import serializers

from api.models import BaseProduct, Category, Parameter, Product, ProductParameter, Shop


class ShopSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    delivery_price = serializers.DecimalField(
        max_digits=19, decimal_places=2, required=False
    )

    class Meta:
        model = Shop
        fields = ["name", "delivery_price", "status"]
        read_only_fields = ["owner", "id"]


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
