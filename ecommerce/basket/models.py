from django.db import models
from users.models import User
from products.models import Products


class Basket(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='User',
                             blank=True,
                             null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created at')

    class Meta:
        verbose_name = 'basket'
        verbose_name_plural = 'Baskets'

    def __str__(self):
        return f'Basket of {self.user.username}'


class BasketItems(models.Model):
    basket = models.ForeignKey(Basket,
                               on_delete=models.CASCADE,
                               verbose_name='Basket',
                               related_name='items')
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE,
                                verbose_name='Product')
    quantity = models.IntegerField(default=0,
                                   verbose_name='Item quantity')
    total_price = models.IntegerField(default=0,
                                      verbose_name='Total price of item')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'Basket items'

    def __str__(self):
        return f'Basket item {self.product.name}'
