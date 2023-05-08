from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItems


@receiver(post_save, sender=OrderItems)
def update_order_total_amount(sender, created, instance, **kwargs):
    if created:
        order = instance.order
        all_products_in_order = OrderItems.objects.filter(order=order)

        order_total_amount = 0
        order_total_bonuses_amount = 0

        for item in all_products_in_order:
            order_total_amount += item.total_price
            order_total_bonuses_amount += item.product.bonuses

        if instance.order.user and instance.order.payment_info.is_paid:
            if instance.order.user.bonuses_balance.balance and instance.order.activate_bonuses:
                user_bonuses = instance.order.user.bonuses_balance.balance
                if user_bonuses >= order_total_amount:
                    instance.order.user.bonuses_balance.balance = user_bonuses - order_total_amount
                    instance.order.user.save()
                    order_total_amount = 0
                elif order_total_amount > user_bonuses > 0:
                    instance.order.user.bonuses_balance.balance = 0
                    instance.order.user.save()
                    order_total_amount -= user_bonuses

        instance.order.total_bonuses_amount = order_total_bonuses_amount
        instance.order.total_amount = order_total_amount
        instance.order.save()
