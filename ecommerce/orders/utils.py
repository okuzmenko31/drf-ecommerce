from basket.utils import BasketMixin, BasketOperationTypes
from payment.services import paypal_create_order
from .models import OrderItems, Order
from users.models import UserShippingInfo
from products.models import Products, AvailabilityStatuses
from rest_framework.response import Response


class OrderMixin(BasketMixin):
    """
    Mixin which creates order with items
    from user's basket. Creates order and
    returns response with order data or
    with error message. Also mixin have method
    which gets or creates user's shipping
    info and returns it.

    TODO: to create receipts method.
    """
    items_serializer = None
    operation_type = BasketOperationTypes.basket_clear
    __request = None

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request):
        self.__request = request

    @staticmethod
    def get_not_available_basket_products(basket_data: dict) -> list:
        """
        Returns list with products from user's basket
        which are not available at the moment.

        Args:
            basket_data(dict): data with basket information.

        Returns:
            not_available_basket_products(list): list with not available
                                                 products from the basket.
        """
        basket_products_ids = []
        for item in basket_data['items']:
            basket_products_ids.append(item['product'])
        not_available_basket_products = Products.objects.filter(
            id__in=basket_products_ids,
            availability_status=AvailabilityStatuses.out_of_stock[0]
        ).values_list('id')
        return not_available_basket_products

    def create_order(self, response) -> Response:
        """
        Creates order and returns response with order data
        or with problems creating an order.

        Args:
            response: response from create method of ListCreateAPIView.

        Returns:
            Response: response with order data or with its problems.
        """
        basket_data = self.get_basket_data(self.request)
        not_available_basket_products = self.get_not_available_basket_products(basket_data)

        if not len(not_available_basket_products) > 0:
            # order will be crated, if in user's basket
            # don't have product that are not available.

            if len(basket_data['items']) > 0:
                # if user's basket is not empty
                order_id = response.data['id']

                try:
                    order = Order.objects.select_related('user').get(id=order_id)
                except Order.DoesNotExist:
                    return Response({'error': 'Order does not exist!'})

                for item in basket_data['items']:
                    # items['product'] - id of product
                    OrderItems.objects.create(order=order,
                                              product_id=item['product'],
                                              quantity=item['quantity'],
                                              total_price=item['total_price'])

                if response.data['payment_method'] == Order.PAYMENT_METHODS[1][0]:
                    # if payment method is by card, to the response
                    # will be added PayPal payment link
                    value = response.data['total_amount']
                    response.data['payment_link'] = paypal_create_order(value, order_id)

                order_items = order.items.all().select_related('order',
                                                               'product')
                response.data['order_items'] = self.items_serializer(instance=order_items,
                                                                     many=True).data
                return response
            else:
                return Response({'basket': 'You dont have items in your basket!'})
        else:
            return Response({'not available': 'Some items in your basket are not available'})

    def get_user_shipping_info(self, shipping_info_data: dict, session_id: str) -> UserShippingInfo:
        """
        This method gets or creates user's
        shipping info and returns it.

        Args:
            shipping_info_data(dict): dictionary with order shipping info data.
            session_id(str): session id of user.

        Returns:
            shipping_info(UserShippingInfo): returns user's shipping info.
        """
        if self.request.user.is_authenticated:
            shipping_info, _ = UserShippingInfo.objects.get_or_create(user=self.request.user,
                                                                      defaults=shipping_info_data)
            if not shipping_info.session_id:
                shipping_info.session_id = session_id
                shipping_info.save()
        else:
            shipping_info, _ = UserShippingInfo.objects.get_or_create(session_id=session_id,
                                                                      defaults=shipping_info_data)
        shipping_info.city = shipping_info_data['city']
        shipping_info.post_office = shipping_info_data['post_office']
        shipping_info.save()
        return shipping_info
