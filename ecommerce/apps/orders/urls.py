from django.urls import path, include
from .views import OrderAPIView, OrderPaypalPaymentComplete, OrdersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', viewset=OrdersViewSet, basename='orders_for_admin')

urlpatterns = [
    path('checkout/', OrderAPIView.as_view(), name='checkout'),
    path('order/<int:order_id>/',
         OrderPaypalPaymentComplete.as_view(),
         name='order_payment_complete'),
    path('', include(router.urls))
]
