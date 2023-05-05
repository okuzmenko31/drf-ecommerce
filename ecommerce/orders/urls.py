from django.urls import path
from .views import OrderAPIView

urlpatterns = [
    path('checkout/', OrderAPIView.as_view(), name='checkout')
]
