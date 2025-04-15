from django import template

register = template.Library()

@register.filter
def batch(value, arg):
    if not value:
        return []
    return [value[i:i + arg] for i in range(0, len(value), arg)]
