from django.contrib import admin
from .models import (Products,
                     ProductDescriptionCategory,
                     ProductDescription,
                     ProductCharacteristics,
                     ProductCharacteristicsCategory,
                     ProductPhotos)
from django.utils.safestring import mark_safe


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'get_photo']
    list_display_links = ['id', 'name', 'price']
    list_editable = ['category']
    list_filter = ['category']
    search_fields = ['id', 'name', 'category', 'price']
    readonly_fields = ['get_photo', 'rating', 'slug']

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')

    get_photo.short_description = 'Item image'
