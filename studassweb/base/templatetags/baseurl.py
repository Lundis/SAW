from django import template
from base.models import SiteConfiguration

register = template.Library()


@register.simple_tag
def base_url():
    return SiteConfiguration.instance().base_url


@register.filter
def with_base_url(absolute_url):
    return SiteConfiguration.instance().base_url+absolute_url