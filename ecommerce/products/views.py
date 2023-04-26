from .models import Products, ProductVariations
from .serializers import ProductsSerializer, ProductVariationsSerializer
from categories.permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import viewsets
from rest_framework import generics
from .utils import ProductVariationsMixin


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


class ProductVariationsAPIView(ProductVariationsMixin,
                               generics.ListAPIView):
    queryset = ProductVariations.objects.all()
    serializer_class = ProductVariationsSerializer

    def get_queryset(self):
        return self.get_related_variations(product_id=self.kwargs['product_id'])
