from products.models import AvailabilityStatuses


def check_quantity_and_set_status(instance):
    product = instance.product
    if instance.quantity_in_stock > 25:
        product.availability_status = AvailabilityStatuses.in_stock[0]
    elif instance.quantity_in_stock < 10 and instance.quantity_in_stock != 0:
        product.availability_status = AvailabilityStatuses.low_in_stock[0]
    elif instance.quantity_in_stock == 0:
        product.availability_status = AvailabilityStatuses.out_of_stock[0]
    product.save()
