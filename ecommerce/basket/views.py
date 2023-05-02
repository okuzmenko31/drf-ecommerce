from .basket import SessionBasket
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Products
from django.shortcuts import get_object_or_404
from .utils import BasketMixin, BasketOperationTypes
from .models import Basket, BasketItems
from rest_framework import status


def get_or_create_basket(request, user):
    basket = SessionBasket(request)
    user_basket, _ = Basket.objects.get_or_create(user=user)
    for item in basket:
        BasketItems.objects.get_or_create(basket=user_basket,
                                          product=item['product'],
                                          quantity=item['quantity'],
                                          total_price=item['total_price'])
    basket.clear()


class BasketAPIView(BasketMixin, APIView):

    def get(self, *args, **kwargs):
        data = self.get_basket_data(self.request)
        return Response(data=data, status=status.HTTP_200_OK)


class OperationBasketAPIView(BasketMixin, APIView):
    operation_type = BasketOperationTypes.basket_add

    def get(self, *args, **kwargs):
        product = get_object_or_404(Products, id=kwargs['product_id'])
        data = self.basket_operation(self.request, product)
        return Response(data=data)


class AddToBasketAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.basket_add


class BasketItemAddQuantityAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.item_add_quantity


class BasketItemMinusQuantityAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.item_minus_quantity


class BasketClearAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.basket_clear

    def get(self, *args, **kwargs):
        data = self.basket_operation(self.request)
        return Response(data=data)
