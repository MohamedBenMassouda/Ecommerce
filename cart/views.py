from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Cart
from .serializers import CartItemSerializer, CartSerializer


@api_view(["POST"])
@login_required
def add_to_cart(request):
    if request.data.get("product_id") is None:
        return Response({"message": "Invalid request."})

    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    product = Product.objects.get(pk=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_to_cart(product, quantity)

    return Response({"message": "Product added to cart successfully."})


@api_view(["DELETE"])
def remove_from_cart(request):
    if request.data.get("product_id") is None:
        return Response({"message": "Invalid request."})

    product_id = request.data.get("product_id")

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.remove_from_cart_by_id(product_id)

    return Response({"message": "Product removed from cart successfully."})


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        if created:
            cart.save()

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        cart = Cart.objects.get(user=request.user)
        item = cart.items.get(pk=item_id)
        serializer = CartItemSerializer(item)

        return Response(serializer.data)
