from rest_framework import serializers
from .models import (Products,
                     ProductDescriptionCategory,
                     ProductDescription,
                     ProductCharacteristics,
                     ProductCharacteristicsCategory,
                     ProductPhotos,
                     ProductVariations)


class ProductsSerializer(serializers.ModelSerializer):
    price_with_discount = serializers.ReadOnlyField()  # this is model property
    rating = serializers.DecimalField(read_only=True, decimal_places=1, max_digits=2)

    class Meta:
        model = Products
        fields = ('id', 'name', 'category', 'price', 'price_with_discount', 'description',
                  'photo', 'discount', 'article', 'rating')


class ProductVariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariations
        fields = ('id', 'variation_category_name', 'product_name', 'product_link')
