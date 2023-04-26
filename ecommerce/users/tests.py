from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from users.models import User, UserToken
from users.token import AuthTokenMixin, get_token_data, TokenData, MESSAGES


class UserTokenTests(TestCase):

    def test_create_token(self):
        mixin = AuthTokenMixin()
        mixin.token_type = 'su'
        email = 'test@example.com'
        token_data = mixin._create_token(email)
        self.assertIsNotNone(token_data.token)
        self.assertIsNone(token_data.error)
        token = UserToken.objects.get(token_owner=email,
                                      token_type=mixin.token_type)
        self.assertEqual(token_data.token, token)

    def test_send_tokenized_mail(self):
        mixin = AuthTokenMixin()
        mixin.token_type = 'su'
        mixin.html_message_template = 'users/confirm_email_message.html'
        email = 'test@example.com'
        response = mixin.send_tokenized_mail(email)
        success_message = mixin.get_context(token_type=mixin.token_type)['success_message']
        self.assertEqual(response, success_message)

    def test_token_data(self):
        mixin = AuthTokenMixin()
        mixin.token_type = 'su'
        email = 'test@example.com'
        token_data = mixin._create_token(email)
        response = get_token_data(token_data.token.token, email)
        self.assertEqual(response, TokenData(token=token_data.token))
        token_data.token.expired = True
        token_data.token.save()
        response = get_token_data(token_data.token.token, email)
        self.assertEqual(response, TokenData(error=MESSAGES['token_expired_error']))
        token_data.token.delete()
        response = get_token_data(token_data.token.token, email)
        self.assertEqual(response, TokenData(error=MESSAGES['token_miss_error']))


class RegistrationAPITests(APITestCase):

    def test_registration(self):
        url = reverse('registration')
        data = {
            'email': 'test_user@gmail.com',
            'password': 'Test_password1',
            'password1': 'Test_password1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, 'test_user@gmail.com')


class LoginLogoutAPITests(APITestCase):

    def setUp(self) -> None:
        user = User.objects.create(email='test_user@gmail.com')
        user.set_password('Test_password1')
        user.save()
        Token.objects.create(user=user)

    def test_get_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_login(self):
        url = reverse('login')
        data = {
            'email': 'test_user@gmail.com',
            'password': 'Test_password1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse('logout')
        token = Token.objects.get(user__email='test_user@gmail.com')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthAPITests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test_user@gmail.com')
        self.user.set_password('Test_password1')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_change_email_send(self):
        url = reverse('change_email_send')
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        data = {
            'email': 'test_email@gmail.com'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_send(self):
        url = reverse('send_password_reset')
        data = {
            'email': self.user.email
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ConfirmationWithTokenTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test_user@gmail.com')
        self.user.set_password('Test_password1')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_email_confirm(self):
        auth_token = UserToken.objects.create(token_owner=self.user.email, token_type='su')
        url = reverse('confirm-email', kwargs={'token': auth_token,
                                               'email': self.user.email})
        response = self.client.get(url)
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_email_confirm(self):
        auth_token = UserToken.objects.create(token_owner=self.user.email, token_type='ce')
        url = reverse('change_email_confirm', kwargs={'token': auth_token,
                                                      'email': self.user.email})
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_password_reset(self):
        auth_token = UserToken.objects.create(token_owner=self.user.email, token_type='pr')
        url = reverse('password_reset', kwargs={'token': auth_token,
                                                'email': self.user.email})
        response = self.client.get(url)
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_password_reset(self):
        auth_token = UserToken.objects.create(token_owner=self.user.email, token_type='pr')
        url = reverse('password_reset', kwargs={'token': auth_token,
                                                'email': self.user.email})
        data = {
            'password': 'Test_password1',
            'password1': 'Test_password1'
        }
        response = self.client.post(url, data, format='json')
        token_data = get_token_data(auth_token, self.user.email)
        if token_data.token:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='test_user@gmail.com')
        self.user.set_password('Test_password1')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid token')

    def test_get_user_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_user_profile(self):
        url = reverse('profile')
        data = {
            'username': 'new_username',
            'full_name': 'Full name'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserBonusesTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='user@gmail.com')
        self.user.set_password('Test_password1')
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid token')
        self.admin = User.objects.create(email='test_admin@gmail.com',
                                         is_staff=True,
                                         is_admin=True)
        self.admin.set_password('Password_admin1')
        self.admin.save()
        Token.objects.create(user=self.admin)

    def test_user_bonuses_balance(self):
        url = reverse('bonuses_balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_update_user_bonuses_balance(self):
        url = reverse('update_bonuses_balance-detail', kwargs={'pk': self.user.bonuses_balance.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_bonuses_balance(self):
        url = reverse('update_bonuses_balance-detail', kwargs={'pk': self.user.bonuses_balance.id})
        data = {
            'user': self.user.bonuses_balance.id,
            'balance': '10000'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin.auth_token.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
