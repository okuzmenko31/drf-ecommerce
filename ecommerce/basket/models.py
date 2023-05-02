from django.db import models
from products.models import Products
from users.models import User


class Basket(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                blank=True,
                                null=True,
                                related_name='basket')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created at')

    class Meta:
        verbose_name = 'basket'
        verbose_name_plural = 'Baskets'

    def __str__(self):
        return f'Basket of {self.user.username}'

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_quantity_of_products(self):
        return sum(item.quantity for item in self.items.all())


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

    def save(self, *args, **kwargs):
        if self.product.discount:
            self.total_price = self.product.price_with_discount * self.quantity
        else:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
