from django.db import models
from apps.products.models import Products
from apps.users.models import UserShippingInfo, User


class Order(models.Model):
    ORDER_STATUSES = (
        (1, 'New'),
        (2, 'Processing'),
        (3, 'Ready to ship'),
        (4, 'Shipped'),
        (5, 'Delivered'),
        (6, 'Canceled')
    )
    PAYMENT_METHODS = (
        (1, 'By cash'),
        (2, 'By card')
    )
    DELIVERY_METHODS = (
        (1, 'Courier'),
        (2, 'To the post office')
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             related_name='orders',
                             blank=True,
                             null=True)
    email = models.EmailField(verbose_name='Email for invoice sending',
                              blank=True,
                              null=True)
    session_id = models.CharField(max_length=32,
                                  blank=True,
                                  null=True)
    order_id = models.CharField(max_length=7,
                                blank=True,
                                null=True)
    order_status = models.IntegerField(verbose_name='Order status',
                                       choices=ORDER_STATUSES,
                                       default=1)
    coupon = models.CharField(max_length=15,
                              verbose_name='Coupon',
                              blank=True,
                              null=True)
    total_amount = models.IntegerField(default=0,
                                       verbose_name='Total amount of order')
    total_bonuses_amount = models.IntegerField(default=0,
                                               verbose_name='Total amount of bonuses for order')
    shipping_info = models.ForeignKey(UserShippingInfo,
                                      on_delete=models.SET_NULL,
                                      verbose_name='User shipping info',
                                      blank=True,
                                      null=True)
    payment_method = models.IntegerField(default=1,
                                         choices=PAYMENT_METHODS,
                                         verbose_name='Payment method')
    delivery_method = models.IntegerField(default=2,
                                          choices=DELIVERY_METHODS,
                                          verbose_name='Delivery method')
    activate_bonuses = models.BooleanField(default=False,
                                           verbose_name='Activate bonuses')
    create_account = models.BooleanField(default=False,
                                         verbose_name='Create an account')
    comment = models.TextField(max_length=1000,
                               verbose_name='Comment',
                               blank=True,
                               null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['total_amount']

    def __str__(self):
        return f'Order #: {self.id}, order_id: {self.id}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name='Order',
                              related_name='items')
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE,
                                verbose_name='Product')
    quantity = models.IntegerField(default=0,
                                   verbose_name='Quantity')
    total_price = models.IntegerField(default=0,
                                      verbose_name='Total price')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'Items in order'
        ordering = ['total_price']

    def __str__(self):
        return f'Item: {self.product.name}, Order: {self.order}'
