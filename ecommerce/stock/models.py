from django.db import models
from products.models import Products
from categories.models import Category


class StockItems(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE,
                                verbose_name='Product',
                                related_name='stock_info')
    product_category = models.ForeignKey(Category,
                                         on_delete=models.CASCADE,
                                         verbose_name='Product category',
                                         blank=True,
                                         null=True)
    price_per_item = models.IntegerField(default=0, verbose_name='Price per item')
    product_article = models.CharField(max_length=8,
                                       verbose_name='Product article',
                                       blank=True,
                                       null=True)
    quantity_in_stock = models.PositiveIntegerField(default=0,
                                                    verbose_name='Quantity in stock')
    quantity_sold = models.PositiveIntegerField(default=0,
                                                verbose_name='Quantity sold')
    stock_date = models.DateTimeField(verbose_name='Stock date',
                                      blank=True,
                                      null=True)
    last_sales_date = models.DateTimeField(verbose_name='Last sales date',
                                           blank=True,
                                           null=True)

    class Meta:
        verbose_name = 'stock item'
        verbose_name_plural = 'Stock items'

    @property
    def product_price_with_discount(self):
        return self.product.price_with_discount

    def save(self, *args, **kwargs):
        self.product_article = self.product.article
        self.product_category = self.product.category
        super().save(*args, **kwargs)
