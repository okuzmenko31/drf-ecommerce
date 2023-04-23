from .models import Products
from .serializers import ProductsSerializer
from categories.permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import viewsets


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
