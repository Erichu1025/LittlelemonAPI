# LittleLemonAPI/templatetags/cart_filters.py

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except:
        return 0


@register.filter
def sum_cart(cart_items):
    """
    Sum the total price in a queryset of cart items,
    each having a quantity and a unit_price.
    """
    return sum(item.quantity * item.unit_price for item in cart_items)