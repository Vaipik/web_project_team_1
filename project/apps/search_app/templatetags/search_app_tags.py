from typing import List

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='highlight')
def highlight(text: str, search_string: str):
    searches = search_string.split()
    for search in searches:
        if isinstance(text, list):
            text = [highlight(el, search_string) for el in text]
        else:
            text = text.replace(search, f'<mark style="background: yellow">{search}</mark>')
    return mark_safe(text)


@register.filter(name='attr')
def attr(item, attribute):

    return mark_safe(vars(item)[attribute])


@register.filter(name='width')
def width(fields):

    return mark_safe(str(12 // len(fields)))
