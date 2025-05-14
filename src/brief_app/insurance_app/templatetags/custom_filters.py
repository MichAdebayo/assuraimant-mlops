from django import template

register = template.Library()


@register.filter
def time_range(value):
    return [f"{hour:02d}:00" for hour in range(9, 19)]
