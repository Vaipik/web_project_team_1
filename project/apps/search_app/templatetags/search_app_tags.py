from typing import List

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='highlight')
def highlight(text: str, searches: List[str]):
    for search in searches:
        if isinstance(text, list):
            text = [highlight(el, searches) for el in text]
        else:
            text = text.replace(search, f'<mark>{search}</mark>')
    return mark_safe(text)


@register.filter(name='attr')
def attr(item, attribute):

    return mark_safe(vars(item)[attribute])
