from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductsViewSet,
                    ProductVariationsAPIView,
                    ProductVariationsByParentAPIView)

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('variations/<int:product_id>/',
         ProductVariationsAPIView.as_view(),
         name='product_variations'),
    path('variations/<int:product_id>/<int:parent_id>/',
         ProductVariationsByParentAPIView.as_view(),
         name='product_variations_by_parent'),
    path('by_category/<int:category_id>/',
         ProductsViewSet.as_view({'get': 'by_category'}),
         name='products_by_category')
]
