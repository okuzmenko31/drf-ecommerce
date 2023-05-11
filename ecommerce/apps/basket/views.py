from .basket import SessionBasket
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from apps.products.models import Products, AvailabilityStatuses
from django.shortcuts import get_object_or_404
from .utils import BasketMixin, BasketOperationTypes
from .models import Basket, BasketItems
from rest_framework import status


def get_or_create_basket(request, user):
    """
    This function is used to get the basket from
    the session and create it in the database.

    Args:
        request (Request): The user's request.
        user (User): User instance.
    """
    basket = SessionBasket(request)
    user_basket, _ = Basket.objects.get_or_create(user=user)
    for item in basket:
        BasketItems.objects.get_or_create(basket=user_basket,
                                          product=item['product'],
                                          quantity=item['quantity'],
                                          total_price=item['total_price'])
    basket.clear()


class BasketAPIView(BasketMixin, APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, *args, **kwargs):
        data = self.get_basket_data(self.request)
        if len(data['items']) > 0:
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response({'basket': 'You dont have items in your basket!'})


class OperationBasketAPIView(BasketMixin, APIView):
    """
    This method is a parent class for other Basket
    Operations API endpoints and is not used in URLs,
    therefore it has no associated link. It defines the
    operation_type attribute which is used to specify the type
    of basket operation to perform. The get method calls
    the basket_operation method of the BasketMixin class with
    the request and product arguments to perform the specified
    basket operation and returns the resulting data as a response.
    """

    def post(self, *args, **kwargs):
        product = get_object_or_404(Products, id=kwargs['product_id'])
        if product.availability_status != AvailabilityStatuses.out_of_stock[0]:
            data = self.basket_operation(self.request, product)
            return Response(data=data)
        else:
            return Response({'not available': 'This product now is not in stock now'})


class AddToBasketAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.basket_add


class BasketItemAddQuantityAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.item_add_quantity


class BasketItemMinusQuantityAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.item_minus_quantity


class BasketClearAPIView(OperationBasketAPIView):
    operation_type = BasketOperationTypes.basket_clear

    def get(self, *args, **kwargs):
        data = self.get_basket_data(self.request)
        return Response(data=data)

    def post(self, *args, **kwargs):
        data = self.basket_operation(self.request)
        return Response(data=data)
