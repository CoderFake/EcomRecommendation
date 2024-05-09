from django import template

register = template.Library()

@register.simple_tag
def calculate_discount(mrp, price):
    try:
        discount = (mrp - price) / mrp * 100
        return round(discount, 2)
    except ZeroDivisionError:
        return 0
