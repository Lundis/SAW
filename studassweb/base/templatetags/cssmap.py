from django import template
from base.models import CSSMap

register = template.Library()


@register.simple_tag
def get_css(key):
    return CSSMap.get(key)
