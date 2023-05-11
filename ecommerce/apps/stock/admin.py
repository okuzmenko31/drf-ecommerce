from django.contrib import admin
from .models import StockItems


@admin.register(StockItems)
class StockItemsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'product_category', 'quantity_in_stock', 'product_article']
    list_display_links = ['id', 'quantity_in_stock']
    list_editable = ['product', 'product_category']
    search_fields = ['id', 'product', 'product_category', 'product_article']

