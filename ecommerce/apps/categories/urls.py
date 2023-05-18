from django.urls import path
from .views import CategoriesViewSet
from rest_framework.routers import DefaultRouter
from django.urls import include

router = DefaultRouter()
router.register(r'', viewset=CategoriesViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls))
]
