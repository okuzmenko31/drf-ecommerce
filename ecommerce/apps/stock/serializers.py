from rest_framework import serializers
from .models import StockItems
from django.urls import reverse


class StockItemsSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    product_price = serializers.CharField(source='product.price',
                                          read_only=True)
    product_category_name = serializers.SerializerMethodField(read_only=True)
    product_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StockItems
        fields = ['id', 'product', 'product_name', 'product_link', 'product_category_name',
                  'product_price', 'product_article', 'quantity_in_stock',
                  'quantity_sold', 'stock_date', 'last_sales_date']
        read_only_fields = ['product_article']

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_link(self, obj):
        return reverse('products-detail', kwargs={'pk': obj.product.pk})

    def get_product_category_name(self, obj):
        return obj.product_category.name
