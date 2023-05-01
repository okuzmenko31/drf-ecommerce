from .models import Products, ProductVariations
from .serializers import ProductsSerializer, ProductVariationsSerializer
from categories.permissions import IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .utils import ProductVariationsMixin


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    @action(detail=False, methods=['get'])
    def by_category(self, reqeust, category_id):
        products = Products.objects.filter(category_id=category_id)
        serializer = ProductsSerializer(instance=products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductVariationsAPIView(ProductVariationsMixin,
                               generics.ListAPIView):
    queryset = ProductVariations.objects.all()
    serializer_class = ProductVariationsSerializer

    def get_queryset(self):
        self.reset_related_variations()
        return self.get_related_variations(product_id=self.kwargs['product_id'])


class ProductVariationsByParentAPIView(ProductVariationsAPIView):
    """
    Endpoint for returning variations of product,
    but filtered by parent_id.
    'parent_id' - id of ParentOfVariationCategory model instance
    """

    def get_queryset(self):
        return self.get_related_variations_by_parent(product_id=self.kwargs['product_id'],
                                                     parent_id=self.kwargs['parent_id'])
