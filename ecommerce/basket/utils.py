from typing import Optional, Union
from basket.basket import SessionBasket
from basket.models import BasketItems, Basket
from basket.serializers import BasketItemsSerializer, SessionBasketSerializer, BasketSerializer
from basket.basket import (basket_add_item,
                           basket_item_add_quantity,
                           basket_item_minus_quantity,
                           basket_remove_item,
                           clear_basket)


class BasketOperationTypes:
    basket_add = 'add'
    item_add_quantity = 'add_quantity'
    item_minus_quantity = 'minus quantity'
    basket_clear = 'clear'


class BasketMixin:
    _basket_data = {}
    operation_type: Optional[str] = None
    __basket: Union[SessionBasket, Basket]

    def basket_add_item(self, request, product):
        if not request.user.is_authenticated:
            self.__basket = SessionBasket(request)
            self.__basket.add(product)
        else:
            self.__basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_add_item(self.__basket, product)

    def basket_add_item_quantity(self, request, product):
        if not request.user.is_authenticated:
            self.__basket = SessionBasket(request)
            self.__basket.add_quantity(product)
        else:
            self.__basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_item_add_quantity(self.__basket, product)

    def basket_minus_item_quantity(self, request, product):
        if not request.user.is_authenticated:
            self.__basket = SessionBasket(request)
            self.__basket.minus_quantity(product)
        else:
            self.__basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_item_minus_quantity(self.__basket, product)

    def basket_remove_item(self, request, product):
        if not request.user.is_authenticated:
            self.__basket = SessionBasket(request)
            self.__basket.remove(product)
        else:
            self.__basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_remove_item(self.__basket, product)

    def basket_clear(self, request):
        if not request.user.is_authenticated:
            self.__basket = SessionBasket(request)
            self.__basket.clear()
        else:
            self.__basket, _ = Basket.objects.get_or_create(user=request.user)
            clear_basket(self.__basket)

    def get_basket_data(self, basket, session_basket=False, model_basket=False):
        if session_basket:
            serializer = SessionBasketSerializer(basket)
            self._basket_data = serializer.data
        else:
            items = BasketItems.objects.filter(basket=basket)
            items_serializer = BasketItemsSerializer(instance=items, many=True)
            self._basket_data = items_serializer.data
        return self._basket_data

    def get_basket(self, request):
        if not request.user.is_authenticated:
            self.__basket = SessionBasket(request)
            basket_data = self.get_basket_data(self.__basket, session_basket=True)
            data = {'basket': basket_data,
                    'total_amount': self.__basket.total_amount,
                    'total_quantity_of_products': len(self.__basket)}
        else:
            self.__basket, _ = Basket.objects.get_or_create(user=request.user)
            basket_data = self.get_basket_data(self.__basket, model_basket=True)
            basket_serializer = BasketSerializer(instance=self.__basket)
            data = {'basket': basket_serializer.data,
                    'items': basket_data,
                    'total_amount': self.__basket.total_amount,
                    'total_quantity_of_products': self.__basket.total_quantity_of_products}
        return data

    def basket_operation(self, request, product=None):
        data = self.get_basket(request)

        if self.operation_type == BasketOperationTypes.basket_add:
            self.basket_add_item(request, product)
        elif self.operation_type == BasketOperationTypes.item_add_quantity:
            self.basket_add_item_quantity(request, product)
        elif self.operation_type == BasketOperationTypes.item_minus_quantity:
            self.basket_minus_item_quantity(request, product)
        elif self.operation_type == BasketOperationTypes.basket_clear:
            self.basket_clear(request)
        return data
