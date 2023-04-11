from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics, status
from .serializers import RegistrationSerializer, LoginSerializer
from .permissions import IsNotAuthenticated
from rest_framework.views import APIView
from .models import User
from .utils import TokenMixin, ConfirmationMailMixin


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


class ConfirmEmailView(TokenMixin,
                       APIView):
    permission_classes = [IsNotAuthenticated]

    def get(self, *args, **kwargs):
        token = self.kwargs.pop('token')
        email = self.kwargs.pop('email')
        response_msg = self.check_token(token, email)
        return Response(response_msg)


class LoginView(APIView):
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
