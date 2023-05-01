import copy
from django.conf import settings
from products.models import Products
from basket.models import BasketItems, Basket
from typing import NamedTuple, Optional


class SessionBasket:

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION)

        if not basket:
            basket = self.session[settings.BASKET_SESSION] = {}
        self.basket = basket

    def save(self):
        self.session[settings.BASKET_SESSION] = self.basket
        self.session.modified = True

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {
                'quantity': 0,
                'price': product.price,
                'price_with_discount': product.price_with_discount
            }
        self.basket[product_id]['quantity'] += 1
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def add_quantity(self, product):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] += 1
        self.save()

    def minus_quantity(self, product):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] -= 1
        self.save()

    def __iter__(self):
        basket_product_ids = self.basket.keys()
        products = Products.objects.filter(id__in=basket_product_ids)
        basket = copy.deepcopy(self.basket)

        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            if item['product'].discount:
                item['total_price'] = item['price_with_discount'] * item['quantity']
            else:
                item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Counting all products in the cart"""
        return sum(item['quantity'] for item in self.basket.values())

    @property
    def total_amount(self):
        """
        Getting overall total price of all
        products in the cart
        """
        return sum(item['price'] for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION]
        self.session.modified = True


class BasketItemData(NamedTuple):
    item: Optional[BasketItems] = None
    exist: Optional[bool] = None


def check_basket_item(basket, product):
    product_id = product.id
    if BasketItems.objects.filter(basket=basket, product_id=product_id).exists():
        item = BasketItems.objects.get(basket=basket,
                                       product_id=product_id)
        return BasketItemData(item=item, exist=True)
    return BasketItemData(exist=False)


def get_or_create_basket_item(basket, product: Products) -> BasketItemData:
    product_id = product.id
    item_data = check_basket_item(basket, product)
    if item_data.item and item_data.exist:
        item = BasketItems.objects.get(basket=basket,
                                       product_id=product_id)
    else:
        item = BasketItems.objects.create(basket=basket,
                                          product=product,
                                          quantity=1,
                                          total_price=product.price)
        return BasketItemData(item=item, exist=True)
    return BasketItemData(item, exist=False)


def basket_add_item(basket, product):
    basket_item_data = get_or_create_basket_item(basket, product)
    if basket_item_data.exist:
        basket_item_data.item.quantity = 1
        basket_item_data.item.save()
    else:
        basket_item_data.item.quantity += 1
        basket_item_data.item.save()


def basket_remove_item(basket, product):
    try:
        item = BasketItems.objects.get(basket=basket,
                                       product_id=product.id)
        item.delete()
    except BasketItems.DoesNotExist:
        return False
    return True


def basket_item_add_quantity(basket, product):
    basket_item_data = check_basket_item(basket, product)
    if basket_item_data.item and basket_item_data.exist:
        basket_item_data.item.quantity += 1
    basket_item_data.item.save()


def basket_item_minus_quantity(basket, product):
    basket_item_data = check_basket_item(basket, product)
    if basket_item_data.item and basket_item_data.exist:
        if basket_item_data.item.quantity > 0:
            basket_item_data.item.quantity -= 1
            basket_item_data.item.save()
        else:
            basket_remove_item(basket, product)


def clear_basket(basket):
    try:
        items = BasketItems.objects.filter(basket=basket)
        for item in items:
            item.delete()
        return True
    except Basket.DoesNotExist:
        return False
