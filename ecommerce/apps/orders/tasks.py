from celery import app
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .services import draw_pdf_invoice
from .models import Order

email_sender = settings.EMAIL_HOST_USER


@app.shared_task
def order_send_email_with_invoice(message, subject, email, order_id, html):
    order = Order.objects.get(id=order_id)
    invoice = draw_pdf_invoice(order)

    email = EmailMultiAlternatives(message,
                                   subject,
                                   email_sender,
                                   [email])
    email.attach('invoice.pdf', invoice, 'application/pdf')
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=True)
