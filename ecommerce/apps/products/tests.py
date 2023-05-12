from rest_framework.test import APITestCase
from apps.products.utils import ProductVariationsMixin
from apps.products.models import (ProductVariations,
                                  Products,
                                  VariationCategory,
                                  ParentOfVariationCategory)
from apps.categories.models import Category
from django.shortcuts import reverse


class TestVariations(ProductVariationsMixin,
                     APITestCase):

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
        self.parent_variation_category = ParentOfVariationCategory.objects.create(name='Memory category')
        self.parent_variation_category2 = ParentOfVariationCategory.objects.create(name='Color category')
        self.variant_category1 = VariationCategory.objects.create(name='Memory 128GB',
                                                                  value='128GB',
                                                                  parent=self.parent_variation_category)
        self.variant_category2 = VariationCategory.objects.create(name='Color Space Black',
                                                                  value='Space Black',
                                                                  parent=self.parent_variation_category2)
        self.variant_category3 = VariationCategory.objects.create(name='Color Deep Purple',
                                                                  value='Deep Purple',
                                                                  parent=self.parent_variation_category2)
        self.first_product_variant1 = ProductVariations.objects.create(variation_category=self.variant_category1,
                                                                       product=self.first_product)
        self.first_product_variant2 = ProductVariations.objects.create(variation_category=self.variant_category2,
                                                                       product=self.first_product)
        self.second_product_variant1 = ProductVariations.objects.create(variation_category=self.variant_category1,
                                                                        product=self.second_product)
        self.second_product_variant2 = ProductVariations.objects.create(variation_category=self.variant_category3,
                                                                        product=self.second_product)

    def test_get_related_variations(self):
        response = list(self.get_related_variations(self.first_product.id).values_list('id',
                                                                                       flat=True))
        product_variation_categories_ids = self.first_product.variations.all().values_list('variation_category_id')
        expected_result = list(ProductVariations.objects.filter(product_id=self.second_product.id).exclude(
            variation_category__in=product_variation_categories_ids
        ).values_list('id', flat=True))
        self.assertEqual(response, expected_result)

    def test_related_variations_endpoint(self):
        url = reverse('product_variations', kwargs={'product_id': self.first_product.id})
        response = self.client.get(url)
        response_result = [item.get('id') for item in response.data]
        product_variation_categories_ids = self.first_product.variations.all().values_list('variation_category_id')
        expected_result = list(ProductVariations.objects.filter(product_id=self.second_product.id).exclude(
            variation_category__in=product_variation_categories_ids
        ).values_list('id', flat=True))
        self.assertEqual(response_result, expected_result)

    def test_get_related_variations_by_parent(self):
        response = list(
            self.get_related_variations_by_parent(self.first_product.id,
                                                  parent_id=self.parent_variation_category2.id).values_list('id',
                                                                                                            flat=True))
        product_variation_categories_ids = self.first_product.variations.all().values_list('variation_category_id')
        expected_result = list(ProductVariations.objects.filter(
            product_id=self.second_product.id,
            variation_category__parent_id=self.parent_variation_category2.id).exclude(
            variation_category__in=product_variation_categories_ids
        ).values_list('id', flat=True))
        self.assertEqual(response, expected_result)

    def test_related_variations_by_parent_endpoint(self):
        url = reverse('product_variations_by_parent', kwargs={'product_id': self.first_product.id,
                                                              'parent_id': self.parent_variation_category2.id})
        response = self.client.get(url)
        response_result = [item.get('id') for item in response.data]
        product_variation_categories_ids = self.first_product.variations.all().values_list('variation_category_id')
        expected_result = list(ProductVariations.objects.filter(
            product_id=self.second_product.id,
            variation_category__parent_id=self.parent_variation_category2.id).exclude(
            variation_category__in=product_variation_categories_ids
        ).values_list('id', flat=True))
        self.assertEqual(response_result, expected_result)


