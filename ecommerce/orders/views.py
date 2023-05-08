from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .serializers import OrderSerializer, OrderItemsSerializer
from .models import Order, OrderItems
from basket.utils import BasketMixin
from rest_framework.permissions import AllowAny
from payment.services import paypal_create_order
from payment.services import paypal_complete_payment


class OrderAPIView(BasketMixin, ListCreateAPIView):
    serializer_class = OrderSerializer
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
        basket_data = self.get_basket_data(request)
        if len(basket_data['items']) > 0:
            response = super().create(request, *args, **kwargs)
            order_id = response.data['id']

            try:
                order = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                return Response({'error': 'Order does not exist!'})

            if response.data['payment_method'] == Order.PAYMENT_METHODS[1][0]:
                value = response.data['total_amount']
                response.data['payment_link'] = paypal_create_order(value, order_id)
            order_items = OrderItems.objects.filter(order=order)
            response.data['order_items'] = OrderItemsSerializer(instance=order_items,
                                                                many=True).data
            return response
        else:
            return Response({'basket': 'You dont have items in your basket!'})


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
