from rest_framework import serializers
from .models import PaymentInfo


class PaymentInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentInfo
        fields = ('id', 'shipping_info', 'payment_method',
                  'payment_amount', 'payment_date', 'is_paid')
        read_only_fields = ('shipping_info', 'payment_amount', 'payment_date')
