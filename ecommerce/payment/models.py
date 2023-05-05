from django.db import models
from orders.models import Order
from users.models import UserShippingInfo


class PaymentInfo(models.Model):
    order = models.OneToOneField(Order,
                                 on_delete=models.CASCADE,
                                 verbose_name='Order',
                                 related_name='payment_info')
    shipping_info = models.ForeignKey(UserShippingInfo,
                                      on_delete=models.SET_NULL,
                                      verbose_name='User shipping info',
                                      blank=True,
                                      null=True)
    payment_method = models.IntegerField(choices=Order.PAYMENT_METHODS,
                                         verbose_name='Payment method')
    payment_amount = models.IntegerField(default=0,
                                         verbose_name='Payment amount')
    payment_date = models.DateTimeField(verbose_name='Payment date',
                                        blank=True,
                                        null=True)
    is_paid = models.BooleanField(default=False,
                                  verbose_name='Order is paid')

    class Meta:
        verbose_name = 'payment info'
        verbose_name_plural = 'Payment infos'

    def __str__(self):
        return f'Payment info order id:{self.order_id}'
