from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'update_bonuses', UpdateUserBonusesBalanceViewSet, basename='update_bonuses_balance')

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('confirm_email/<token>/<email>/', ConfirmEmailAPIView.as_view(), name='confirm-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change_email/', ChangeEmailAPIView.as_view(), name='change_email_send'),
    path('change_email_confirm/<token>/<email>/',
         ChangeEmailConfirmAPIView.as_view(),
         name='change_email_confirm'),
    path('password_reset/', SendPasswordResetAPIView.as_view(), name='send_password_reset'),
    path('password_reset/<token>/<email>/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('bonuses_balance/', UserBonusesBalanceAPIView.as_view(), name='bonuses_balance'),
    path('', include(router.urls))
]
