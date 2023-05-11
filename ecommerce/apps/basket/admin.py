from django.contrib import admin
from .models import Basket, BasketItems


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketItems)
class BasketItemsAdmin(admin.ModelAdmin):
    pass
