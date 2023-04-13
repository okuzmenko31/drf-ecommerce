from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import (RegistrationSerializer,
                          LoginSerializer,
                          ChangeEmailSerializer,
                          SendPasswordResetMailSerializer,
                          PasswordResetSerializer,
                          ProfileSerializer,
                          UserBonusesSerializer)
from .permissions import IsNotAuthenticated
from rest_framework.views import APIView
from .models import User, UserToken, UserBonusesBalance
from .utils import TokenMixin, ConfirmationMailMixin
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication


class UserRegistrationAPIView(TokenMixin,
                              ConfirmationMailMixin,
                              generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]
    token_type = 'su'

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': self.get_success_message(self.token_type),
            'data': response.data
        }, status=status.HTTP_200_OK)


class ConfirmEmailAPIView(TokenMixin,
                          APIView):
    permission_classes = [IsNotAuthenticated]
    token_type = 'su'

    def get(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        if self.check_token(token, email):
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            return Response({'success': 'You successfully confirmed your email!'},
                            status=status.HTTP_200_OK)
        else:
            error_msg = self.check_token_error_msg(token, email)
            return Response(data=error_msg['error'], status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [IsNotAuthenticated]

    def get(self, *args, **kwargs):
        data = {
            'user': str(self.request.user),
            'auth': str(self.request.auth)
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        password = self.request.data['password']
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            data = {
                'message': 'Successful authentication',
                'token': user.auth_token.key
                # we can call user.auth_token because in Token model
                # have related_name="auth_token" to user instance.
                # you can check it here 'rest_framework.authtoken.models'.
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Provided email or password is wrong!'},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, *args, **kwargs):
        user = self.request.user
        user.auth_token.delete()
        user_tokens = UserToken.objects.filter(token_owner=user.email, expired=False)
        for token in user_tokens:
            token.delete()
        try:
            logout(self.request)
        except User.DoesNotExist:
            return Response({'error': 'Logout error'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'You successfully logged out!'}, status=status.HTTP_200_OK)


class ChangeEmailAPIView(TokenMixin,
                         ConfirmationMailMixin,
                         APIView):
    serializer_class = ChangeEmailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    token_type = 'ce'
    html_message_template = 'users/confirm_email_changing.html'

    def post(self, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        self.token_owner = self.request.user.email
        self.send_confirmation_mail(email, self.get_token())
        return Response({'success': self.get_success_message(self.token_type)})


class ChangeEmailConfirmAPIView(TokenMixin,
                                ConfirmationMailMixin,
                                APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    token_type = 'ce'

    def get(self, *args, **kwargs):
        token = kwargs.pop('token')
        new_email = kwargs.pop('email')
        if self.check_token(token, self.request.user.email):
            user = self.request.user
            user.email = new_email
            user.save()
            msg = {'success': 'You successfully changed your email'}
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg = self.check_token_error_msg(token, self.request.user.email)
            return Response(data=msg, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetAPIView(TokenMixin,
                               ConfirmationMailMixin,
                               APIView):
    serializer_class = SendPasswordResetMailSerializer
    token_type = 'pr'
    html_message_template = 'users/password_reset_msg.html'

    def post(self, *args, **kwargs):
        serializer = SendPasswordResetMailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        self.token_owner = email
        self.send_confirmation_mail(email, self.get_token())
        return Response({'success': self.get_success_message(self.token_type)},
                        status=status.HTTP_200_OK)


class PasswordResetAPIView(TokenMixin,
                           APIView):
    serializer_class = PasswordResetSerializer
    token_type = 'pr'

    def get(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        if self.check_token(token, email):
            return Response({'message': 'Password reset page. Write new password.'},
                            status=status.HTTP_200_OK)
        else:
            return Response(data=self.check_token_error_msg(token, email),
                            status=status.HTTP_400_BAD_REQUEST)

    def post(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        if self.check_token(token, email):
            serializer = PasswordResetSerializer(data=self.request.data, context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            return Response({'success': 'Password reset success.'},
                            status=status.HTTP_200_OK)
        else:
            return Response(data=self.check_token_error_msg(token, email),
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()

    def get_object(self):
        user = self.queryset.get(id=self.request.user.id)
        return user

    def perform_update(self, serializer):
        if '@' not in self.request.data['username']:
            username = '@' + self.request.data['username']
            serializer.save(username=username)


class UserBonusesBalanceAPIView(generics.ListAPIView):
    serializer_class = UserBonusesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = UserBonusesBalance.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
