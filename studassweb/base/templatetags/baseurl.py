# coding=utf-8
from django import template
from base.models import SiteConfiguration

register = template.Library()


@register.simple_tag
def base_url():
    """

    :return:
    """
    return SiteConfiguration.instance().base_url


@register.filter
def with_base_url(absolute_url):
    """

    :param absolute_url:
    :return:
    """
    return SiteConfiguration.instance().base_url+absolute_url
