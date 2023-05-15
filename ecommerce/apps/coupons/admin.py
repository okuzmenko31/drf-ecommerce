from django.contrib import admin
from .models import Coupons, UserCoupons

@admin.register(Coupons)
class CouponsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'discount']
    list_display_links = ['id']
    list_editable = ['product']
    search_fields = ['id', 'product', 'coupon', 'discount']
    exclude = ['coupon']


admin.site.register(UserCoupons)
