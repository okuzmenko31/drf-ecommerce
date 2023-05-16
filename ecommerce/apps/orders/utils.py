from apps.basket.utils import BasketMixin, BasketOperationTypes
from apps.payment.services import paypal_create_order
from .models import OrderItems, Order
from apps.users.models import UserShippingInfo
from apps.products.models import Products, AvailabilityStatuses
from rest_framework.response import Response
from django.db.models import Sum
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .services import draw_pdf_invoice
from apps.products.services import get_discount
from .tasks import order_send_email_with_invoice

email_sender = settings.EMAIL_HOST_USER


class OrderMixin(BasketMixin):
    """
    Mixin which creates order with items
    from user's basket. Creates order and
    returns response with order data or
    with error message. Also, mixin have method
    which gets or creates user's shipping
    info and returns it. And to all this, there is
    a method for sending an invoice to the mail.
    """
    items_serializer = None
    operation_type = BasketOperationTypes.basket_clear
    __request = None
    invoice_html_template = 'orders/invoice_msg.html'
    send_invoice_with_celery = False

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

    @staticmethod
    def get_order_total_values(order: Order) -> dict:
        """
        This method returns dict with order
        total amount and total bonuses amount.
        """
        total_values_order = order.items.aggregate(total_amount=Sum('total_price'),
                                                   total_bonuses_amount=Sum('product__bonuses'))
        return total_values_order

    def process_order_payment_with_bonuses(self, order: Order):
        """
        Processes the payment for the given order
        using user bonuses balance and updates the
        payment status and order total amount accordingly.
        """
        order_total_values = self.get_order_total_values(order)

        order_total_amount = order_total_values['total_amount']
        order_total_bonuses_amount = order_total_values['total_bonuses_amount']

        if order.user and order.activate_bonuses and order.user.bonuses_balance:
            # bonuses will be withdrawn from the user's bonuses balance
            # only if he has selected this option
            user_bonuses = order.user.bonuses_balance.balance

            if user_bonuses >= order_total_amount:
                # if the user's balance is greater than the
                # total amount of the order, the total amount
                # of order will be deducted from user's bonuses
                # balance and order will be marked as paid.
                order.user.bonuses_balance.balance = user_bonuses - order_total_amount
                order.user.bonuses_balance.save()

                payment_info = order.payment_info
                payment_info.is_paid = True
                payment_info.save()

                if order_total_bonuses_amount > 0:
                    # add order bonuses to the user's balance
                    # we have the same operation in payment/signals.py in
                    # pre save signal, but in this case it won't be working
                    # because initially order not is_paid what is needed to call
                    # pre save method
                    order.user.bonuses_balance.balance += order_total_bonuses_amount
                    order.user.bonuses_balance.save()
                    payment_info.bonus_taken = True

                payment_info.payment_amount = order_total_amount
                payment_info.save()

            elif order_total_amount > user_bonuses > 0:
                order.user.bonuses_balance.balance = 0
                order.user.bonuses_balance.save()
                order_total_amount -= user_bonuses

        order.total_bonuses_amount = order_total_bonuses_amount
        order.total_amount = order_total_amount
        order.save()

    def order_total_amount_with_coupon(self, order: Order) -> bool:
        """
        This method counts order total amount
        if order have coupon.

        Args:
            order(Order): order instance.

        Returns:
            bool: True or false depending on whether the total
                  amount of the order has been changed.
        """
        order_total_values = self.get_order_total_values(order)
        order_total_amount = order_total_values['total_amount']

        if order.user and order.coupon and order.coupon.is_active:
            order_total_amount = get_discount(order_total_amount, order.coupon.coupon.discount)
            order.total_amount = order_total_amount
            order.coupon.is_active = False
            order.coupon.save()
            order.save()
            return True
        return False

    def send_email_with_invoice(self, order: Order):
        html = render_to_string(self.invoice_html_template, {'order': order})
        invoice = draw_pdf_invoice(order)

        subject = 'DRF ECOMMERCE'
        message = f'Invoice for order# {order.id}'
        if self.send_invoice_with_celery:
            order_send_email_with_invoice.delay(message=message,
                                                subject=subject,
                                                email=order.shipping_info.email,
                                                order_id=order.id,
                                                html=html)
        else:
            email = EmailMultiAlternatives(message, subject, email_sender, [order.shipping_info.email])
            email.attach('invoice.pdf', invoice, 'application/pdf')
            email.attach_alternative(html, 'text/html')
            email.send(fail_silently=True)

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

        if self.request.user.is_authenticated:
            # we need it in this case because in this
            # way we avoid unnecessary access to the cart table.
            self.clear_exist_basket(self.request)
        else:
            self.basket_operation(self.request)

        not_available_basket_products = self.get_not_available_basket_products(basket_data)

        if not len(not_available_basket_products) > 0:
            # order will be created, if in user's basket
            # don't have products that are not available.

            if len(basket_data['items']) > 0:
                # if user's basket is not empty
                order_id = response.data['id']

                try:
                    order = Order.objects.select_related('user').prefetch_related('items').get(id=order_id)
                except Order.DoesNotExist:
                    return Response({'error': 'Order does not exist!'})

                for item in basket_data['items']:
                    # items['product'] - id of product
                    OrderItems.objects.create(order=order,
                                              product_id=item['product'],
                                              quantity=item['quantity'],
                                              total_price=item['total_price'])

                order_items = order.items.all().select_related('order',
                                                               'product')

                if order.coupon and self.order_total_amount_with_coupon(order):
                    # here order total amount with discount from coupon
                    response.data['total_amount'] = order.total_amount
                else:
                    response.data['total_amount'] = order_items.aggregate(
                        total_amount=Sum('total_price'))['total_amount']

                if response.data['payment_method'] == Order.PAYMENT_METHODS[1][0] and not order.payment_info.is_paid:
                    # if payment method is by card, to the response
                    # will be added PayPal payment link
                    value = response.data['total_amount']
                    response.data['payment_link'] = paypal_create_order(value, order_id)
                else:
                    self.process_order_payment_with_bonuses(order)
                    # we are  processing order payment with bonuses here only if
                    # payment method is by cash, to avoid withdrawal
                    # of bonuses without payment(in case if payment method is by card).
                    self.send_email_with_invoice(order)

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
