from django import template
import random

register = template.Library()


@register.simple_tag
def random_number(max_value=100):
    return random.randint(1, max_value)