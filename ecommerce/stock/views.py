from rest_framework.viewsets import ModelViewSet
from core.global_permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import StockItems
from .serializers import StockItemsSerializer


class StockItemsViewSet(ModelViewSet):
    serializer_class = StockItemsSerializer
    queryset = StockItems.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
