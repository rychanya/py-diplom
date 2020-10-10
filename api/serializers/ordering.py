from rest_framework import serializers

from api.models import Cart, CartItem, Order, OrderItem, Product


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(
        max_digits=19, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ["product", "price", "quantity", "total_price"]
        read_only_fields = ["price", "total_price"]

    def create(self, validated_data):
        try:
            product = Product.objects.get(pk=validated_data["product"].id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("product does not exist")
        cart, _ = Cart.objects.get_or_create(user=self.context["request"].user)
        item, _ = CartItem.objects.update_or_create(
            product=product,
            defaults={
                "cart": cart,
                "price": product.price,
                "quantity": validated_data["quantity"],
            },
        )
        item.save()
        return item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source="cartitem_set")

    class Meta:
        model = Cart
        fields = [
            "items",
        ]
        read_only = [
            "items",
        ]


class OrderIteamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    items = OrderIteamSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = "__all__"
