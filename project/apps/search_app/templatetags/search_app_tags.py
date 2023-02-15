import re
from datetime import datetime
from typing import List

from django import template
from django.utils.safestring import mark_safe, SafeString

register = template.Library()


@register.filter(name='highlight')
def highlight(text: str, search_string: str):
    searches = search_string.split()
    for search in searches:
        if isinstance(text, list):
            text = [highlight(el, search_string) for el in text]
        else:
            for i_search in re.findall(search, text, re.I):
                if i_search in text:
                    text = text.replace(i_search, f'<mark style="background: yellow">{i_search}</mark>')
                    break
    return mark_safe(text)


@register.filter(name='attr')
def attr(item, attribute):
    if "__" in attribute:
        fk, field = attribute.split("__")
        try:
            values = [el.__getattribute__(field) for el in item.__getattribute__(fk).all()]
            if len(values) > 1:
                result = ", ".join(values)
            else:
                result = values[0]
        except IndexError:
            result = ""
        return mark_safe(result)
    try:
        result = item.__getattribute__(attribute)
    except IndexError:
        result = ""
    if isinstance(result, datetime):
        result = result.strftime("%Y.%m.%d %H:%M:%S")
    return mark_safe(result)


@register.filter(name='width')
def width(fields):

    return mark_safe(str(12 // len(fields)))
