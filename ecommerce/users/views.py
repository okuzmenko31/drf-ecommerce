from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import RegistrationSerializer, LoginSerializer, ChangeEmailSerializer
from .permissions import IsNotAuthenticated
from rest_framework.views import APIView
from .models import User, UserToken
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
        })


class ConfirmEmailAPIView(TokenMixin,
                          APIView):
    permission_classes = [IsNotAuthenticated]
    token_type = 'su'

    def get(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        if self.check_token(token, email):
            user = self.request.user
            user.is_active = True
            return Response({'success': 'You successfully confirmed your email!'})
        else:
            error_msg = self.check_token_error_msg(token, email)
            return Response(error_msg['error'], status=error_msg['status'])


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

    def get(self, *args, **kwargs):
        return Response({'message': 'Write new email'})

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
