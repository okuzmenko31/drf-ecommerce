from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .serializers import OrderSerializer, OrderItemsSerializer
from .models import Order
from apps.basket.utils import BasketMixin
from rest_framework.permissions import AllowAny
from apps.payment.services import paypal_complete_payment
from .utils import OrderMixin


class OrderAPIView(OrderMixin,
                   BasketMixin,
                   ListCreateAPIView):
    serializer_class = OrderSerializer
    items_serializer = OrderItemsSerializer
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def list(self, request, *args, **kwargs):
        data = self.get_basket_data(request)
        if len(data['items']) > 0:
            return Response(data=data)
        else:
            return Response({'basket': 'You dont have items in your basket!'})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.request = request
        return self.create_order(response)


class OrderPaypalPaymentComplete(APIView):

    def get(self, *args, **kwargs):
        order_id = kwargs['order_id']
        payment_id = self.request.query_params.get('paymentId')
        payer_id = self.request.query_params.get('PayerID')
        if paypal_complete_payment(payment_id, payer_id):
            try:
                order = Order.objects.get(id=order_id)
            except (Exception,):
                return Response({'error': 'Order error.'})
            order.payment_info.is_paid = True
            if order.user and order.total_bonuses_amount > 0:
                order.user.bonuses_balance.balance += order.total_bonuses_amount
                order.user.bonuses_balance.save()
                order.payment_info.bonus_taken = True
            order.payment_info.save()
        return Response({'success': 'You successfully paid for order!'})
