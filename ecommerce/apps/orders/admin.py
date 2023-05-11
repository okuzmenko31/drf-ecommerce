from django.contrib import admin
from .models import Order, OrderItems
from apps.payment.models import PaymentInfo


class PaymentInfoTabularInline(admin.TabularInline):
    model = PaymentInfo


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id']
    list_display_links = ['id', 'order_id']
    inlines = [PaymentInfoTabularInline]


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    pass
