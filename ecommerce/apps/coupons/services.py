import random
from datetime import date


# from .models import Coupons


def generate_end_date(start_date):
    """
    This function returns generated deactivation
    date of coupon.
    """
    s_date = start_date

    if s_date.month < 12:
        end_date_month = random.randint(s_date.month + 1, 12)
        end_date_day = random.randint(1, 25)
        end_date_year = s_date.year
    else:
        end_date_month = random.randint(1, 12)
        end_date_day = random.randint(1, 25)
        end_date_year = s_date.year + 1

    end_date = date(end_date_year, end_date_month, end_date_day)
    return end_date


def get_coupon(coupon) -> bool:
    coupon_drop_chance = coupon.drop_chance
    random_percent = random.uniform(0, 1)

    if random_percent <= coupon_drop_chance:
        return True
    return False
