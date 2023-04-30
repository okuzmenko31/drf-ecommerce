from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:product_id>/', AddToBasketAPIView.as_view())
]
