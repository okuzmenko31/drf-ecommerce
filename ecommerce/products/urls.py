from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductsViewSet,
                    ProductVariationsAPIView)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
    path('variations/<int:product_id>/',
         ProductVariationsAPIView.as_view(),
         name='product_variations')
]
