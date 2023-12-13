from django import template
from django.templatetags.static import static

register = template.Library()


@register.filter(name='image_filter')
def image_filter(value, arg=None):
    if value:
        return value.url
    else:
        return static('images/stub.png')
