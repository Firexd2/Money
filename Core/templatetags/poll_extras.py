from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def points(value):
    value = list(value)
    value.reverse()
    result = []
    for n, digit in enumerate(value, start=1):
        result.append(digit)
        if n % 3 == 0 and n != len(value):
            result.append('.')
    result.reverse()
    return ''.join(result)
