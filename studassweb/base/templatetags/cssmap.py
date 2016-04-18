from django import template
from base.models import CSSMap2

register = template.Library()


@register.simple_tag
def get_css(key):
    return CSSMap2.get(key)
