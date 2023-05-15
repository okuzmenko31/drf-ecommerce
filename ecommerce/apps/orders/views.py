from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .serializers import (OrderSerializer,
                          OrderItemsSerializer,
                          OrdersForAdminSerializer)
from .models import Order
from apps.basket.utils import BasketMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.payment.services import paypal_complete_payment
from .utils import OrderMixin


class OrderAPIView(OrderMixin,
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
        mixin = OrderMixin()
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
            mixin.send_email_with_invoice(order)
        return Response({'success': 'You successfully paid for order!'})


class OrdersViewSet(BasketMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    serializer_class = OrdersForAdminSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Order.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        data = self.get_basket_data(request)
        response.data['items'] = data
        return response
