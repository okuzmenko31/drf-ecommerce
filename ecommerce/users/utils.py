import binascii
import os
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserToken, User
from rest_framework import status
from typing import NamedTuple, Optional, Any

MESSAGES = {
    'token_miss_error': ('This token does not exist or belongs '
                         'to another user!'),
    'token_expired_error': ('Signature expired'),
    'no_user': ('No such user with this email address!'),
    'complete_registration': ('Ecommerce - complete registration.'),
    'complete_email_changing': ('Ecommerce - complete changing email'),
    'complete_password_reset': ('Ecommerce - complete password reset'),
    'registration_mail_sent': ('Mail with registration link has '
                               'been sent to your email.'),
    'email_changing_sent': ('Mail with email changing confirmation '
                            'has been sent to your new email. '
                            'Your email in this account will be '
                            'changed after confirmation.'),

    'password_reset_sent': ('Mail with password reset confirmation has been sent '
                            'to your email.')
}


class TokenData(NamedTuple):
    token: Optional[UserToken] = None
    email: Optional[str] = None
    token_type: Optional[str] = None
    error: Optional[str] = None


class TokenTypes:
    SIGNUP = 'su'
    CHANGE_EMAIL = 'ce'
    PASSWORD_RESET = 'pr'


class MailContextMixin:
    __subject = None
    __message = ''
    __success_message = None

    @classmethod
    def _set_subject(cls, token_type):
        if token_type == 'su':
            cls.__subject = MESSAGES['complete_registration']
        elif token_type == 'ce':
            cls.__subject = MESSAGES['complete_email_changing']
        else:
            cls.__subject = MESSAGES['complete_password_reset']

    @classmethod
    def _set_success_message(cls, token_type):
        if token_type == 'su':
            cls.__success_message = MESSAGES['registration_mail_sent']
        elif token_type == 'ce':
            cls.__success_message = MESSAGES['email_changing_sent']
        else:
            cls.__success_message = MESSAGES['password_reset_sent']

    def get_context(self, token_type):
        self._set_subject(token_type)
        self._set_success_message(token_type)

        context = {
            'subject': self.__subject,
            'message': self.__message,
            'success_message': self.__success_message
        }
        return context


class AuthTokenMixin(MailContextMixin):
    token_type = None
    html_message_template = None

    def create_token(self, email: str) -> TokenData:
        if not UserToken.objects.filter(token_owner=email,
                                        token_type=self.token_type).exists():
            token = UserToken.objects.create(token_owner=email,
                                             token_type=self.token_type)
        else:
            try:
                User.objects.get(token_owner=email,
                                 token_type=self.token_type).delete()
                token = UserToken.objects.create(token_owner=email,
                                                 token_type=self.token_type)
            except UserToken.DoesNotExist:
                return TokenData(error=MESSAGES['token_miss_error'])
        return TokenData(token=token)

    def send_tokenized_mail(self, email: str) -> str:
        mail_context = self.get_context(token_type=self.token_type)
        token_data = self.create_token(email)

        if token_data.error:
            return token_data.error

        cont = {
            'email': str(email),
            'domain': '127.0.0.1:8000',
            'site_name': 'Ecommerce',
            'token': token_data.token.token,
            'protocol': 'http'
        }
        subject = mail_context['subject']
        message = mail_context['message']
        html_msg = render_to_string(self.html_message_template, cont)
        send_mail(subject,
                  message,
                  settings.EMAIL_HOST_USER,
                  [email],
                  html_message=html_msg)
        return mail_context['success_message']

    def get_token_data(self, token: str, email: str) -> TokenData:
        try:
            token = UserToken.objects.get(token=token,
                                          token_owner=email)
            if token.expired:
                return TokenData(error=MESSAGES['token_expired_error'])
            return TokenData(token=token)
        except UserToken.DoesNotExist:
            return TokenData(error=MESSAGES['token_miss_error'])
