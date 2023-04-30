from .basket import SessionBasket
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Products
from django.shortcuts import get_object_or_404


class AddToBasketAPIView(APIView):

    def get(self, *args, **kwargs):
        basket = SessionBasket(self.request)
        product = get_object_or_404(Products, id=kwargs['product_id'])
        basket.add(product)
        basket_items = []
        # for item in basket:
        #     basket_items.append(item)
        # print(basket_items)
        # for item in basket:
        #     print(item)

        return Response({'basket': basket.basket})
