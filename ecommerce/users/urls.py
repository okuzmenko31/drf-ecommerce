from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('confirm_email/<token>/<email>/', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change_email/', ChangeEmailAPIView.as_view(), name='change_email_send'),
    path('change_email_confirm/<token>/<email>/',
         ChangeEmailConfirmAPIView.as_view(),
         name='change_email_confirm')
]
