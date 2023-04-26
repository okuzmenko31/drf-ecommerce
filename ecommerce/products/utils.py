from .models import Products, ProductVariations
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet


class ProductVariationsMixin:
    __product_variations_categories = []
    __variations_categories = []

    def get_related_variations(self, product_id: int) -> QuerySet[ProductVariations]:
        """
        This method returns variations which related with product.
        For example if product have related variation with
        category 'Memory: 128GB' and 'Color: Space Black',
        this method will return variations with category
        'Memory 128GB' but with different color categories.
        This is only example for easiest understanding of
        this method, your variations and variation
        categories may be different.
        """
        product = get_object_or_404(Products, id=product_id)
        for product_variation in product.variations.all():
            self.__product_variations_categories.append(product_variation.variation_category)
        products = Products.objects.filter(category=product.category)
        for item in products:
            for variation in item.variations.all().exclude(variation_category__in=self.__product_variations_categories):
                self.__variations_categories.append(variation.variation_category)
        variations = ProductVariations.objects.filter(variation_category__in=self.__variations_categories).exclude(
            product=product)
        return variations
