from .basket import SessionBasket
from django.conf import settings
from basket.models import Basket, BasketItems


class BasketMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        basket = SessionBasket(request)
        basket_items = []
        for item in basket:
            basket_items.append(item)

        if request.user.is_authenticated:
            basket_from_db, _ = Basket.objects.get_or_create(user=request.user)
            basket.clear()

            for item in basket_items:
                BasketItems.objects.get_or_create(basket=basket_from_db,
                                                  product=item['product'],
                                                  quantity=item['quantity'],
                                                  total_price=item['total_price'])
        response = self.get_response(request)
        return response
