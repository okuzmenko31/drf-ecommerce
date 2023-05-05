from django.contrib import admin
from .models import Order, OrderItems


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id']
    list_display_links = ['id', 'order_id']


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    pass
