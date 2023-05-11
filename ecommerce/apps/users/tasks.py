from celery import app
from django.conf import settings
from django.core.mail import send_mail

email_sender = settings.EMAIL_HOST_USER


@app.shared_task
def celery_send_tokenized_mail(subject, message, email, html_msg):
    send_mail(subject,
              message,
              settings.EMAIL_HOST_USER,
              [email],
              html_message=html_msg)
