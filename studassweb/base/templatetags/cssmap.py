from django.template.base import Library
from base.models import CSSMap

register = Library()


@register.simple_tag
def get_css(key):
    return CSSMap.get(key)
