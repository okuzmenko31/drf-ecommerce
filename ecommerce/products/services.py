def get_discount(price, discount):
    """Calculating discount"""

    discount = float(price * discount / 100)
    total = float(price - discount)
    int_total = int(total)
    return int_total
