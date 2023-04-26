from django.test import TestCase
from rest_framework.test import APITestCase
from products.utils import ProductVariationsMixin
from products.models import ProductVariations, Products, VariationCategory
from categories.models import Category


class TestVariations(ProductVariationsMixin,
                     TestCase):

    def setUp(self) -> None:
        self.main_category = Category.objects.create(name='Smartphones')
        self.subcategory = Category.objects.create(name='Apple Smartphones',
                                                   parent=self.main_category)
        self.last_category = Category.objects.create(name='Apple iPhone 14 Pro',
                                                     parent=self.subcategory)
        self.first_product = Products.objects.create(name='Apple iPhone 14 Pro 128GB Space Black',
                                                     category=self.last_category,
                                                     price=50000,
                                                     discount=2)
        self.second_product = Products.objects.create(name='Apple iPhone 14 Pro 128GB Deep Purple',
                                                      category=self.last_category,
                                                      price=48599,
                                                      discount=1)
        self.variant_category1 = VariationCategory.objects.create(name='Memory 128GB',
                                                                  value='128GB')
        self.variant_category2 = VariationCategory.objects.create(name='Color Space Black',
                                                                  value='Space Black')
        self.variant_category3 = VariationCategory.objects.create(name='Color Deep Purple',
                                                                  value='Deep Purple')
        self.first_product_variant1 = ProductVariations.objects.create(variation_category=self.variant_category1,
                                                                       product=self.first_product)
        self.first_product_variant2 = ProductVariations.objects.create(variation_category=self.variant_category2,
                                                                       product=self.first_product)
        self.second_product_variant1 = ProductVariations.objects.create(variation_category=self.variant_category1,
                                                                        product=self.second_product)
        self.second_product_variant2 = ProductVariations.objects.create(variation_category=self.variant_category3,
                                                                        product=self.second_product)

    def test_related_variants(self):
        """
        TODO: Complete this test.
        """
        response = self.get_related_variations(self.first_product.id)
        expected_result = ProductVariations.objects.filter(variation_category__in=self.__variations_categories).exclude(
            product=self.first_product)
        self.assertEqual(response, expected_result)
