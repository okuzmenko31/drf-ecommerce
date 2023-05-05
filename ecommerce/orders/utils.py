from basket.utils import BasketMixin, BasketOperationTypes
from .models import Order, OrderItems
from users.models import UserShippingInfo
from payment.models import PaymentInfo
from products.models import Products
from django.utils import timezone


class OrderSerializerMixin(BasketMixin):
    operation_type = BasketOperationTypes.basket_clear
    __request = None

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request):
        self.__request = request

    def __clear_basket(self):
        self.basket_operation(self.request)

    def get_user_shipping_info(self, shipping_info_data, session_id):
        if self.request:
            shipping_info, _ = UserShippingInfo.objects.get_or_create(user=self.request.user,
                                                                      defaults=shipping_info_data)
        else:
            shipping_info, _ = UserShippingInfo.objects.get_or_create(session_id=session_id,
                                                                      defaults=shipping_info_data)
        shipping_info.city = shipping_info_data['city']
        shipping_info.post_office = shipping_info_data['post_office']
        shipping_info.save()
        return shipping_info

    def create_order_items(self, order):
        basket_data = self.get_basket_data(self.request)
        for item in basket_data['items']:
            try:
                product = Products.objects.get(id=item['product'])
            except (Exception,):
                raise ValueError('Product does not exist')
            OrderItems.objects.create(order=order,
                                      product=product,
                                      quantity=item['quantity'],
                                      total_price=item['total_price'])
        self.__clear_basket()

    @staticmethod
    def create_payment_info(order: Order):
        PaymentInfo.objects.create(order=order,
                                   shipping_info=order.shipping_info,
                                   payment_method=order.payment_method,
                                   payment_amount=order.total_amount,
                                   payment_date=timezone.now(),
                                   is_paid=False)
