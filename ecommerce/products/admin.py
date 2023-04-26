from django.contrib import admin
from .models import (Products,
                     ProductDescriptionCategory,
                     ProductDescription,
                     ProductCharacteristics,
                     ProductCharacteristicsCategory,
                     ProductPhotos,
                     VariationCategory,
                     ProductVariations)
from django.utils.safestring import mark_safe
from django.forms.models import inlineformset_factory

ProductVariationInlineFormSet = inlineformset_factory(Products,
                                                      ProductVariations,
                                                      fields=('variation_category', 'product'))


class ProductVariationInline(admin.TabularInline):
    model = ProductVariations
    extra = 1
    formset = ProductVariationInlineFormSet


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'get_photo']
    list_display_links = ['id', 'name', 'price']
    list_editable = ['category']
    list_filter = ['category']
    search_fields = ['id', 'name', 'category', 'price']
    readonly_fields = ['get_photo', 'rating', 'slug']
    inlines = [ProductVariationInline]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100" height="100" />')

    get_photo.short_description = 'Item image'


@admin.register(VariationCategory)
class VariationCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['id', 'name']
    exclude = ['slug']


admin.site.register(ProductVariations)
