from rest_framework import serializers
from .models import (Products,
                     ProductDescriptionCategory,
                     ProductDescription,
                     ProductCharacteristics,
                     ProductCharacteristicsCategory,
                     ProductPhotos,
                     ProductVariations,
                     AvailabilityStatuses)


class ProductsSerializer(serializers.ModelSerializer):
    price_with_discount = serializers.ReadOnlyField()  # this is model property
    rating = serializers.DecimalField(read_only=True, decimal_places=1, max_digits=2)
    availability_status = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ('id', 'name', 'category', 'price', 'price_with_discount', 'description',
                  'photo', 'discount', 'article', 'rating', 'availability_status')

    def get_availability_status(self, obj):
        status = ''
        if obj.availability_status == AvailabilityStatuses.in_stock[0]:
            status = AvailabilityStatuses.in_stock[1]
        elif obj.availability_status == AvailabilityStatuses.low_in_stock[0]:
            status = AvailabilityStatuses.low_in_stock[1]
        elif obj.availability_status == AvailabilityStatuses.awaiting_arrival[0]:
            status = AvailabilityStatuses.awaiting_arrival[1]
        else:
            obj.availability_status = AvailabilityStatuses.out_of_stock[1]
        return status


class ProductVariationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariations
        fields = ('id', 'variation_category_name', 'product_name', 'product_link')
