from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer

from core.utils import check_user_is_valid


# Create your views here.
class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if check_user_is_valid(request):
            return Response({"message": "Invalid request."})

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Customer created successfully."})

        else:
            return Response(serializer.errors)


class CustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            
        except Customer.DoesNotExist:
            return Response({"message": "Customer does not exist."})

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
