from django.urls import path
from .views import OrderAPIView, OrderPaypalPaymentComplete

urlpatterns = [
    path('checkout/', OrderAPIView.as_view(), name='checkout'),
    path('order/<int:order_id>/',
         OrderPaypalPaymentComplete.as_view(),
         name='order_payment_complete')
]
