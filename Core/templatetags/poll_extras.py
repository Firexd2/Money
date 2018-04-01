from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from Core.models import HelpText

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
            if value[n] != '-':
                result.append('.')
    result.reverse()
    return ''.join(result)
