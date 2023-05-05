from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from .serializers import OrderSerializer
from .models import Order
from basket.utils import BasketMixin
from basket.permissions import BasketLenMoreThanZeroPermission
from rest_framework.permissions import AllowAny


class OrderAPIView(BasketMixin, ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [BasketLenMoreThanZeroPermission, AllowAny]

    def list(self, request, *args, **kwargs):
        data = self.get_basket_data(request)
        return Response(data=data)
