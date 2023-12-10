from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication

from .models import Product, Category
from .serializers import ProductSerializer


# Create your views here.
class ProductList(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    def post(self, request):
        if not request.user:
            return Response(status=401)

        category = get_object_or_404(Category, name=request.data["category"])

        try:
            product = Product.objects.get(name=request.data["name"], category=category)

            product.stock += 1
            product.save()
        except Product.DoesNotExist:
            product = Product.objects.create(
                category=category,
                name=request.data["name"],
                price=request.data["price"],
                stock=request.data["stock"],
                created_by=request.user,
            )

        serializer = ProductSerializer(product)

        return Response(serializer.data)


class ProductDetail(APIView):
    pass
