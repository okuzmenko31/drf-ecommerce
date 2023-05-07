from django.contrib import admin
from .models import PaymentInfo


@admin.register(PaymentInfo)
class PaymentInfoAdmin(admin.ModelAdmin):
    pass
