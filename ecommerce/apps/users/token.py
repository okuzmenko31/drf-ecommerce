from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserToken, User
from typing import NamedTuple, Optional
from .tasks import celery_send_tokenized_mail

MESSAGES = {
    'token_miss_error': ('This token does not exist or belongs '
                         'to another user!'),
    'token_expired_error': 'Signature expired',
    'no_user': 'No such user with this email address!',
    'complete_registration': 'Ecommerce - complete registration.',
    'complete_email_changing': 'Ecommerce - complete changing email',
    'complete_password_reset': 'Ecommerce - complete password reset',
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
    """
    Mixin which creates context for mail and
    returns success message the content of which
    will depend on the type of token.
    """
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
        """
        Returns context with mail subject, message and
        success message for user that mail has been sent.
        """
        self._set_subject(token_type)
        self._set_success_message(token_type)

        context = {
            'subject': self.__subject,
            'message': self.__message,
            'success_message': self.__success_message
        }
        return context


class AuthTokenMixin(MailContextMixin):
    """
    Mixin for creating and sending tokenized email.

    This mixin provides methods for creating and sending tokens via email for
    various token types. Available token types are:
        - SignUp ['su']
        - Change email ['ce']
        - Password reset ['pr']

    Attributes:
        token_type (str): The token type to create.
        html_message_template (str): The path to the HTML message template.
    """
    token_type = None
    html_message_template = None
    mail_with_celery = False

    def _create_token(self, email: str) -> TokenData:
        """
        Method which creates a new token for the given email.

        Args:
            email (str): The email address to associate with the token.

        Returns:
            TokenData: The TokenData object with either the token or an error message.
        """

        if not UserToken.objects.filter(token_owner=email,
                                        token_type=self.token_type).exists():
            token = UserToken.objects.create(token_owner=email,
                                             token_type=self.token_type)
        else:
            try:
                # If a token already exists, it will be deleted
                # and a new one will be created.
                User.objects.get(token_owner=email,
                                 token_type=self.token_type).delete()
                token = UserToken.objects.create(token_owner=email,
                                                 token_type=self.token_type)
            except UserToken.DoesNotExist:
                return TokenData(error=MESSAGES['token_miss_error'])
        return TokenData(token=token)

    def send_tokenized_mail(self, email: str) -> str:
        """
        Method that calls the `_create_token` method to generate
        a token for the given email address, creates a context
        for an email and sends it to the user's email address.
        Returns a success message upon successful email delivery
        or an error message if an error occurs.

        Args:
            email (str): The email address to which the token email will be sent.

        Returns:
            str: A success message upon successful email delivery
                 or an error message if an error occurs.
        """
        mail_context = self.get_context(token_type=self.token_type)
        token_data = self._create_token(email)

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

        if self.mail_with_celery:
            celery_send_tokenized_mail.delay(subject, message, email, html_msg)
        else:
            send_mail(subject,
                      message,
                      settings.EMAIL_HOST_USER,
                      [email],
                      html_message=html_msg)

        return mail_context['success_message']


def get_token_data(token: str, email: str) -> TokenData:
    """
    Function for getting token data.

    Args:
        token (str): The token string to retrieve.
        email (str): The email of the token owner.

    Returns:
        TokenData: The TokenData object with either the token or an error message.

    Raises:
        Token.DoesNotExist: If the token does not exist.
    """
    try:
        token = UserToken.objects.get(token=token,
                                      token_owner=email)
        if token.expired:
            return TokenData(error=MESSAGES['token_expired_error'])
        return TokenData(token=token)
    except UserToken.DoesNotExist:
        return TokenData(error=MESSAGES['token_miss_error'])
