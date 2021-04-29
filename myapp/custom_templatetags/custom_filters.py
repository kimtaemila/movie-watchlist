from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def char_at(value: str, index: int) -> str:
    """Returns the character from a string at the given index."""
    if len(value) > int(index):
        return value[index]


@register.filter(is_safe=True)
@stringfilter
def starts_with_alphabet(value: str) -> bool:
    initial_char = char_at(value, 0)
    if ord(initial_char) in range(65, 90) or ord(initial_char) in range(97, 122):
        return True
    return False


@register.filter(is_safe=True)
def display_as(value, name: str) -> str:
    if name == 'language':
        match = re.match(r'(?P<language>.+)(?=\s\((?P<country>.+)\))',
                         value.get_language_display())
        return match.groupdict()['language']

    elif name == 'type':
        return value.get_type_display()

    elif name == 'fullname':
        fullname = value.get_full_name()
        if fullname == '':
            return value.username

        return fullname


@register.filter(is_safe=True)
@stringfilter
def vartype(value, name: str):
    if name == 'type':
        return type(value)


@register.filter(is_safe=True)
def test(value):
    return None


@register.filter(is_safe=True)
def is_empty(value):
    if len(value) > 0:
        return False

    return True
