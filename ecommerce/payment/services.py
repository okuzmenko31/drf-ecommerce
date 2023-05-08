import requests
import base64
import os
import paypalrestsdk
from dotenv import load_dotenv
from django.utils import timezone
from orders.models import Order
from payment.models import PaymentInfo

load_dotenv()

client = paypalrestsdk.configure(
    {
        "mode": "sandbox",
        "client_id": os.getenv('PAYPAL_CLIENT_ID'),
        "client_secret": os.getenv('PAYPAL_CLIENT_SECRET'),
    }
)


def get_paypal_access_token(client_id, client_secret):
    url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic {0}".format(base64.b64encode((client_id + ":" + client_secret).encode()).decode())
    }

    token = requests.post(url, data, headers=headers)
    return token.json()['access_token']


access_token = get_paypal_access_token(os.getenv('PAYPAL_CLIENT_ID', 'your_client_id'),
                                       os.getenv('PAYPAL_CLIENT_SECRET', 'your_client_secret'))


def paypal_create_order(value, order_id):
    payment_url = None
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(value),
                "currency": "USD"
            },
            "description": f"Payment for order #{order_id}"
        }],
        "redirect_urls": {
            "return_url": f'http://127.0.0.1:8000/api/v1/orders/order/{order_id}',
            "cancel_url": f'http://127.0.0.1:8000/api/v1/orders/order/{order_id}'
        }
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                payment_url = link.href
    else:
        return payment.error
    return payment_url


def paypal_complete_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        return True
    else:
        return False


def create_payment_info(order: Order):
    PaymentInfo.objects.create(order=order,
                               shipping_info=order.shipping_info,
                               payment_method=order.payment_method,
                               payment_amount=order.total_amount,
                               payment_date=timezone.now(),
                               is_paid=False)
