import binascii
import os
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserToken, User
from rest_framework import status

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


class TokenTypes:
    SIGNUP = 'su'
    CHANGE_EMAIL = 'ce'
    PASSWORD_RESET = 'pr'


class TokenMixin:
    __token = None
    __token_owner = None
    token_type = None

    @staticmethod
    def _token_types():
        token_types = []
        for token_type in UserToken.TOKEN_TYPES:
            token_types.append(token_type[0])
        return token_types

    def _check_token_type(self):
        if self.token_type not in self._token_types():
            return False
        return True

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(16)).decode()

    def create_token(self):
        if self._check_token_type():
            if UserToken.objects.filter(token=self.__token, token_owner=self.__token_owner).exists():
                UserToken.objects.get(token=self.__token,
                                      token_owner=self.__token_owner).delete()
                self.__token = UserToken.objects.create(token=self.generate_token(),
                                                        token_type=self.token_type,
                                                        token_owner=self.__token_owner)
            else:
                self.__token = UserToken.objects.create(token=self.generate_token(),
                                                        token_type=self.token_type,
                                                        token_owner=self.__token_owner)
        return self.__token

    @property
    def token_owner(self):
        return self.__token_owner

    @token_owner.setter
    def token_owner(self, email):
        self.__token_owner = email
        self.create_token()

    def get_token(self):
        return self.__token

    def check_token_error_msg(self, token_value, email):
        try:
            token = UserToken.get_token_from_str(token_value, email)
            if token.expired:
                return {'error': MESSAGES['token_expired_error']}
        except UserToken.DoesNotExist:
            return {'error': MESSAGES['token_miss_error']}
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return {'error': MESSAGES['no_user']}

    def check_token(self, token_value, email):
        try:
            token = UserToken.get_token_from_str(token_value, email)
            if token.expired:
                return False
        except UserToken.DoesNotExist:
            return False
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return False
        self.delete_token(token_value, email)
        return True

    @staticmethod
    def delete_token(token, email):
        try:
            token = UserToken.get_token_from_str(token, email)
            token.delete()
        except UserToken.DoesNotExist:
            raise ValueError('Token Does Not Exist!')


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


class ConfirmationMailMixin(MailContextMixin):
    mail_with_celery = False
    html_message_template = None

    def send_confirmation_mail(self, email, token: UserToken):
        mail_context = self.get_context(token.token_type)
        cont = {
            'email': str(email),
            'domain': '127.0.0.1:8000',
            'site_name': 'Ecommerce',
            'token': token.token,
            'protocol': 'http'
        }
        subject = mail_context['subject']
        message = mail_context['message']
        html_msg = render_to_string(self.html_message_template, cont)

        if self.mail_with_celery:
            pass
        else:
            send_mail(subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      html_message=html_msg)

    def get_success_message(self, token_type):
        context = self.get_context(token_type)
        success_message = context['success_message']
        return success_message
