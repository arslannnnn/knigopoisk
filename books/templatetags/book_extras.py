from django import template

register = template.Library()

@register.filter
def star_width(value):
    try:
        rating = float(value)
    except (TypeError, ValueError):
        return 0

    width = rating * 10
    if width < 0:
        width = 0
    if width > 100:
        width = 100

    return int(width)
