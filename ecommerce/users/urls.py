from django.urls import path
from .views import *

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('confirm_email/<token>/<email>/', ConfirmEmailView.as_view(), name='confirm-email'),
    path('login/', LoginView.as_view(), name='login')
]
