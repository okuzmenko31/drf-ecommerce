from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=250,
                            verbose_name='Name',
                            unique=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            verbose_name='Parent',
                            blank=True,
                            null=True,
                            related_name='children')
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']
        
    def __str__(self):
        return f'Category: {self.name}'
