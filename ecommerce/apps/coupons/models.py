import binascii
import os
from django.db import models
from apps.products.models import Products
from apps.users.models import User
from .services import generate_end_date
from django.utils import timezone


class Coupons(models.Model):
    coupon = models.CharField(max_length=16,
                              verbose_name='Coupon',
                              blank=True,
                              null=True)
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE,
                                verbose_name='Product',
                                related_name='coupons')
    discount = models.PositiveSmallIntegerField(default=1,
                                                verbose_name='Discount')
    drop_chance = models.PositiveSmallIntegerField(default=1,
                                                   verbose_name='Chance to drop')

    class Meta:
        verbose_name = 'coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['discount']

    def __str__(self):
        return f'Coupon for: {self.product.name}'

    @staticmethod
    def generate_coupon():
        return binascii.hexlify(os.urandom(8)).decode()

    def save(self, *args, **kwargs):
        if self._state.adding and (not self.coupon or Coupons.objects.filter(coupon=self.coupon).exists()):
            self.coupon = self.generate_coupon().upper()
        super().save(*args, **kwargs)


class UserCoupons(models.Model):
    coupon = models.ForeignKey(Coupons,
                               on_delete=models.CASCADE,
                               verbose_name='Coupon')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             related_name='coupons')
    started_at = models.DateField(auto_now_add=True,
                                  verbose_name='Coupon start date')
    valid_to = models.DateField(verbose_name='Coupon valid to',
                                blank=True,
                                null=True)
    is_active = models.BooleanField(default=True,
                                    verbose_name='Is active')

    class Meta:
        verbose_name = 'user coupon'
        verbose_name_plural = "Users' coupons"

    def __str__(self):
        return f'Coupon of: {self.user.username}'

    def save(self, *args, **kwargs):
        if self.started_at is None:
            self.started_at = timezone.now()
        self.valid_to = generate_end_date(self.started_at)
        super().save(*args, **kwargs)
