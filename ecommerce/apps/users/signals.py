from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserBonusesBalance


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        UserBonusesBalance.objects.create(user=instance)
