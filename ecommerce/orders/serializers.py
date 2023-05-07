from rest_framework import serializers
from orders.models import Order, OrderItems
from products.models import Products
from products.serializers import ProductsSerializer
from users.serializers import UserShippingInfoSerializer
from users.models import UserShippingInfo
from basket.utils import BasketMixin, BasketOperationTypes
from .utils import OrderSerializerMixin


class OrderItemsSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()
    product = ProductsSerializer()

    class Meta:
        model = OrderItems
        fields = ('order_id', 'product', 'quantity', 'total_price')

    def get_order_id(self, obj):
        return obj.order.order_id


class OrderSerializer(OrderSerializerMixin,
                      serializers.ModelSerializer):
    shipping_info = UserShippingInfoSerializer()

    class Meta:
        model = Order
        fields = ('id', 'shipping_info',
                  'payment_method', 'delivery_method',
                  'coupon', 'activate_bonuses',
                  'comment', 'create_account',
                  'total_amount')
        read_only_fields = ['total_amount']

    def create(self, validated_data):
        shipping_info_data = validated_data.pop('shipping_info')
        request = self.context.get('request')
        session_id = request.session.session_key
        self.request = request

        shipping_info = self.get_user_shipping_info(shipping_info_data, session_id)
        order = Order.objects.create(shipping_info=shipping_info, **validated_data)

        self.create_order_items(order)

        if request.user.is_authenticated:
            order.user = request.user
            order.save()
        else:
            order.session_id = session_id
            order.save()
        self.create_payment_info(order)
        return order
