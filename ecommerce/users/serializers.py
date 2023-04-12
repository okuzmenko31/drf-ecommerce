from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from .utils import TokenMixin, ConfirmationMailMixin
from rest_framework.authtoken.models import Token


class RegistrationSerializer(TokenMixin,
                             ConfirmationMailMixin,
                             serializers.Serializer):
    token_type = 'su'
    html_message_template = 'users/confirm_email_message.html'

    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password])
    password1 = serializers.CharField(write_only=True,
                                      required=True,
                                      validators=[validate_password])

    def validate(self, attrs):
        if attrs['password1'] != attrs['password']:
            raise serializers.ValidationError('Password mismatch.')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('User with this email is already exists!')
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create(email=email, is_active=False)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)  # creating authentication token
        self.token_owner = email
        self.send_confirmation_mail(email, self.get_token())
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            if user.auth_token:
                user.auth_token.delete()
            Token.objects.create(user=user)  # creating authentication token
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError('The password is wrong!')
        except User.DoesNotExist:
            raise serializers.ValidationError('No such user with this email!')
        return attrs


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(label='New E-mail',
                                   write_only=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())],
                                   required=True)

    def validate(self, attrs):
        email = attrs['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email is already exists')
        return attrs
