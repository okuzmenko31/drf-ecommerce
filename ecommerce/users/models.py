from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=250,
                                verbose_name='Username',
                                unique=True,
                                blank=True,
                                null=False)
    email = models.EmailField(unique=True,
                              verbose_name='E-mail',
                              null=False)
    full_name = models.CharField(max_length=250,
                                 verbose_name='Full name',
                                 blank=True,
                                 null=True)
    is_staff = models.BooleanField(verbose_name='Staff status', default=False)
    is_superuser = models.BooleanField(verbose_name='Superuser status', default=False)
    is_active = models.BooleanField(verbose_name='User activated', default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(verbose_name='Last login', null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='Date joined', auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username}, {self.full_name}'

    def save(self, *args, **kwargs):
        if self._state.adding and (
                not self.username or User.objects.filter(username=self.username).exists()
        ):
            email = self.email
            self.username = User.objects.generate_username(email)
        super(User, self).save(*args, **kwargs)


class UserToken(models.Model):
    TOKEN_TYPES = (
        ('su', 'SignUp token'),
        ('ce', 'Change email token'),
        ('pr', 'Password reset token')
    )
    token = models.CharField(unique=True,
                             max_length=32,
                             verbose_name='Token',
                             blank=True,
                             null=True)
    token_type = models.CharField(max_length=2, choices=TOKEN_TYPES,
                                  verbose_name='Token type',
                                  blank=True,
                                  null=True)
    token_owner = models.EmailField(verbose_name='Token owner email',
                                    blank=True,
                                    null=True)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Token creation date')
    expired = models.BooleanField(default=False,
                                  verbose_name='Token expired')

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'Tokens'

    def __str__(self):
        return f'{self.token}, {self.token_type}'


class UserBonusesBalance(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                verbose_name='User',
                                related_name='bonuses_balance')
    balance = models.IntegerField(default=0,
                                  verbose_name='User balance')

    def __str__(self):
        return f'{self.balance}$'
