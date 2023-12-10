from rest_framework import serializers

from products.serializers import ProductSerializer
from .models import Cart, CartItem


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['items'] = CartItemSerializer(instance.items.all(), many=True).data

        return representation


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data

        return representation
