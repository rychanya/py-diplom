from rest_framework import serializers

from api.models import (
    BaseProduct,
    Category,
    Parameter,
    Product,
    ProductParameter,
    Shop,
    User,
)


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


class ProductParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product.name")

    class Meta:
        model = ProductParameter
        fields = ["name", "value"]


class ProductFileSerializer(serializers.ModelSerializer):
    parameters = ProductParameterSerializer(many=True)
    id = serializers.IntegerField()
    category = serializers.IntegerField()
    name = serializers.CharField()

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
        name = validated_data.pop("name")
        category_id = validated_data.pop("category")
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                f"category with id {category_id} does not exist"
            )
        base_product, _ = BaseProduct.objects.get_or_create(
            name=name, category=category
        )
        validated_data["base"] = base_product
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
        user = User(
            email=validated_data["email"],
            username=validated_data["email"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            middle_name=validated_data["middle_name"],
            company=validated_data["company"],
            position=validated_data["position"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user