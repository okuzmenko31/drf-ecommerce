from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockItemsViewSet

router = DefaultRouter()
router.register(r'', StockItemsViewSet, basename='stock_items')

urlpatterns = [
    path('', include(router.urls))
]
