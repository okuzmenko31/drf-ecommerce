from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemsSerializer
from .models import Order, OrderItems
from basket.utils import BasketMixin
from basket.permissions import BasketLenMoreThanZeroPermission
from rest_framework.permissions import AllowAny
from payment.services import paypal_create_order
from payment.services import paypal_complete_payment


class OrderAPIView(BasketMixin, ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [BasketLenMoreThanZeroPermission, AllowAny]

    def list(self, request, *args, **kwargs):
        data = self.get_basket_data(request)
        return Response(data=data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        order_id = response.data['id']
        if response.data['payment_method'] == Order.PAYMENT_METHODS[1][0]:
            value = response.data['total_amount']
            response.data['payment_link'] = paypal_create_order(value, order_id)
        order_items = OrderItems.objects.filter(order_id=order_id)
        response.data['order_items'] = OrderItemsSerializer(instance=order_items,
                                                            many=True).data
        return response


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
            order.payment_info.save()
        return Response({'success': 'You successfully paid for order!'})
