from django.db import models
from categories.models import Category
from .services import get_discount
from django.utils.text import slugify


class ProductDescriptionCategory(models.Model):
    name = models.CharField(verbose_name='Description category name',
                            unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Products descriptions categories'

    def __str__(self):
        return f'Description category: {self.name}'


class ProductDescription(models.Model):
    description_category = models.ForeignKey(ProductDescriptionCategory,
                                             on_delete=models.CASCADE,
                                             blank=True,
                                             null=True,
                                             verbose_name='Description category')
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Description')

    class Meta:
        verbose_name = 'description'
        verbose_name_plural = 'Descriptions'

    def __str__(self):
        return f'Description of: {self.products.name}'


class ProductCharacteristicsCategory(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Name',
                            unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Characteristics category'

    def __str__(self):
        return f'Characteristics category: {self.name}'


class ProductCharacteristics(models.Model):
    """
    Model of characteristics of any product.
    For example: 'Model: MacBook Air 13 2020' - this is one characteristic.
    """
    characteristics_category = models.ForeignKey(ProductCharacteristicsCategory,
                                                 on_delete=models.CASCADE,
                                                 verbose_name='Category',
                                                 blank=True,
                                                 null=True,
                                                 related_name='characteristics')
    product = models.ForeignKey('Products',
                                on_delete=models.CASCADE,
                                verbose_name='Product',
                                related_name='characteristics',
                                null=False)
    name = models.CharField(blank=True,
                            null=True,
                            verbose_name='characteristics name')
    value = models.CharField(max_length=200,
                             verbose_name='Value')

    class Meta:
        verbose_name = 'description'
        verbose_name_plural = 'Descriptions'

    def __str__(self):
        return f'Description of: {self.product.name}'


class Products(models.Model):
    name = models.CharField(max_length=350,
                            verbose_name='Name')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 verbose_name='Category',
                                 related_name='products',
                                 blank=True,
                                 null=True)
    price = models.IntegerField(default=0,
                                verbose_name='Price')
    description = models.ForeignKey(ProductDescription,
                                    on_delete=models.CASCADE,
                                    verbose_name='Description',
                                    related_name='products',
                                    blank=True,
                                    null=True)
    photo = models.ImageField(upload_to='images/products/',
                              verbose_name='Photo',
                              blank=True,
                              null=True)
    discount = models.IntegerField(default=0,
                                   verbose_name='Discount(Optional)')
    article = models.CharField(max_length=8,
                               verbose_name='Article',
                               blank=True)
    slug = models.SlugField(unique=True,
                            verbose_name='Slug')
    rating = models.DecimalField(max_digits=2,
                                 decimal_places=1,
                                 verbose_name='Rating',
                                 default=0)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def price_with_discount(self):
        """
        Returns calculated price with discount.
        """
        price_with_discount = get_discount(self.price, self.discount)
        return price_with_discount


class ProductPhotos(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE,
                                verbose_name='Product',
                                related_name='photos')
    photo = models.ImageField(upload_to='images/products/all/',
                              verbose_name='Product photos',
                              blank=True,
                              null=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'Photos'

    def __str__(self):
        return f'Photo of: {self.product.name}'
