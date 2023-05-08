from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PaymentInfo


@receiver(pre_save, sender=PaymentInfo)
def accrue_to_user_balance(sender, instance, **kwargs):
    if instance.order.user:
        if instance.order.total_bonuses_amount and instance.is_paid and not instance.bonus_taken:
            instance.order.user.bonuses_balance.balance += instance.order.total_bonuses_amount
            instance.order.user.bonuses_balance.save()
            instance.bonus_taken = True
            instance.save()
