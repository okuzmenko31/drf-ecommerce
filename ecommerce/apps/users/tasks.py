from datetime import timedelta

from celery import app
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import UserToken

email_sender = settings.EMAIL_HOST_USER


@app.shared_task
def celery_send_tokenized_mail(subject, message, email, html_msg):
    send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
              [email],
              html_message=html_msg)


@app.shared_task
def delete_expired_tokens():
    expiration_data = timezone.now() - timedelta(hours=2)
    expired_tokens = UserToken.objects.filter(created__lt=expiration_data)
    expired_tokens.delete()
