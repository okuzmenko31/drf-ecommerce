from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderItems


@receiver(post_save, sender=OrderItems)
def update_order_total_amount(sender, instance, **kwargs):
    order = instance.order
    all_products_in_order = OrderItems.objects.filter(order=order)

    order_total_amount = 0

    for item in all_products_in_order:
        order_total_amount += item.total_price
    instance.order.total_amount = order_total_amount
    instance.order.save()
