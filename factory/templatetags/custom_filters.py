from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieve value from a dictionary by key in Django templates."""
    return dictionary.get(key, 0)
