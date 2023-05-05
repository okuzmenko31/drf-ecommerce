from rest_framework import serializers
from orders.models import Order, OrderItems
from products.models import Products
from products.serializers import ProductsSerializer
from users.serializers import UserShippingInfoSerializer
from users.models import UserShippingInfo
from basket.utils import BasketMixin, BasketOperationTypes


class OrderItemsSerializer(serializers.ModelSerializer):
    order_id = serializers.SerializerMethodField()
    product = ProductsSerializer()

    class Meta:
        model = OrderItems
        fields = ('order_id', 'product', 'quantity', 'total_price')

    def get_order_id(self, obj):
        return obj.order.order_id


class OrderSerializer(BasketMixin, serializers.ModelSerializer):
    operation_type = BasketOperationTypes.basket_clear

    shipping_info = UserShippingInfoSerializer()

    class Meta:
        model = Order
        fields = ('shipping_info', 'payment_method', 'delivery_method',
                  'coupon', 'activate_bonuses',
                  'comment', 'create_account')

    def create(self, validated_data):
        shipping_info_data = validated_data.pop('shipping_info')
        request = self.context.get('request')
        session_id = request.session.session_key
        if request.user.is_authenticated:
            shipping_info, _ = UserShippingInfo.objects.get_or_create(user=request.user,
                                                                      defaults=shipping_info_data)
        else:
            shipping_info, _ = UserShippingInfo.objects.get_or_create(session_id=session_id,
                                                                      defaults=shipping_info_data)
        shipping_info.city = shipping_info_data['city']
        shipping_info.post_office = shipping_info_data['post_office']
        shipping_info.save()

        order = Order.objects.create(shipping_info=shipping_info, **validated_data)

        basket_data = self.get_basket_data(request)
        for item in basket_data['items']:
            try:
                product = Products.objects.get(id=item['product'])
            except (Exception,):
                raise ValueError('Product does not exist')
            OrderItems.objects.create(order=order, product=product,
                                      quantity=item['quantity'], total_price=item['total_price'])

        if request.user.is_authenticated:
            order.user = request.user
            order.save()
        else:
            order.session_id = session_id
            order.save()

        self.basket_operation(request)
        return order
