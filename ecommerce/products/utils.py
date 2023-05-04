from .models import Products, ProductVariations
from django.db.models import QuerySet


class ProductVariationsMixin:
    _related_variations = []

    def reset_related_variations(self):
        """
        This method helps to avoid bug with related variations.
        If you don't reset variations before getting them,
        your list with related variations won't be updated.
        It means that every time when you will try to get variations of some
        product, and after you will try to get variations of another,
        you will get mixed variations of these products.
        """
        self._related_variations = []

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
        TODO: Optimize queries
        """
        product = Products.objects.select_related('category').get(id=product_id)
        related_variations = ProductVariations.objects.filter(
            variation_category__in=product.variations.values('variation_category'),
            product__category=product.category).select_related('product', 'variation_category',
                                                               'product__category').exclude(product=product).distinct(
            'product')
        for variation in related_variations:
            another_variations = variation.product.variations.select_related('variation_category').exclude(
                variation_category=variation.variation_category).values_list('id', flat=True)
            self._related_variations.extend(another_variations)
        variations = ProductVariations.objects.filter(
            id__in=self._related_variations).select_related('product', 'variation_category').exclude(product=product)
        return variations

    def get_related_variations_by_parent(self, product_id: int, parent_id: int) -> QuerySet[ProductVariations]:
        """
        This method is similar to 'get_related_variations' method,
        but returns filtered variations by provided parent_id.
        'parent_id' - id of ParentOfVariationCategory model instance.
        """
        variations = self.get_related_variations(product_id)
        variations_by_parent = variations.filter(variation_category__parent_id=parent_id). \
            select_related('product', 'product__category')
        return variations_by_parent
