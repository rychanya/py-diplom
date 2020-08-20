from rest_framework import serializers

from .models import Category, Parameter, Product, ProductParameter, Shop


class CategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField()

    def create(self, validated_data):
        category, _ = Category.objects.update_or_create(
            pk=validated_data["id"], defaults={"name": validated_data["name"]}
        )
        return category

    def validate(self, data):
        if Category.objects.filter(name=data["name"]).exclude(pk=data["id"]).exists():
            raise serializers.ValidationError(f"Category with this name already exist.")
        return data


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "owner"]


class ProductParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")

    class Meta:
        model = ProductParameter
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    parameters = ProductParameterSerializer(many=True)
    id = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "model",
            "name",
            "quantity",
            "price",
            "price_rrc",
            "parameters",
        ]

    def create(self, validated_data):
        parameters = validated_data.pop("parameters")
        product_id = validated_data.pop("id")
        product, _ = Product.objects.update_or_create(
            pk=product_id, defaults=validated_data
        )
        for parameter in parameters:
            param, _ = Parameter.objects.get_or_create(
                name=parameter["product"]["name"]
            )
            ProductParameter.objects.update_or_create(
                product=product, parameter=param, defaults={"value": parameter["value"]}
            )
        return product
