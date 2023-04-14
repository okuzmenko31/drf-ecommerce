from django.db import models
from categories.models import Category


class ProductDescription(models.Model):
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='Description')

    class Meta:
        verbose_name = 'description'
        verbose_name_plural = 'Descriptions'

    def __str__(self):
        return f'Description of: {self.product.name}'


class ProductCharactheristicsCategory(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Name',
                            unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Charactherisctics category'

    def __str__(self):
        return f'Charactherisctics category: {self.name}'


class ProductCharactheristics(models.Model):
    charactheristic_category = models.ForeignKey(ProductCharactheristicsCategory,
                                                 on_delete=models.CASCADE,
                                                 verbose_name='Category',
                                                 blank=True,
                                                 null=True,
                                                 related_name='charactherisctics')
    product = models.ForeignKey('Products',
                                on_delete=models.CASCADE,
                                verbose_name='Product',
                                related_name='charactheristics',
                                null=False)
    name = models.CharField(blank=True,
                            null=True,
                            verbose_name='Charactheristic name')
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
                                    related_name='products')
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
                                 verbose_name='Rating')
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f'{self.name}'
    
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
