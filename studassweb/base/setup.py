# coding=utf-8
from .utils import get_modules_with
from .models import CSSMap2

__author__ = 'Lundis'


def setup_css_map():
    """
    Register css strings from all modules
    :return:
    """
    modules = get_modules_with("register", "get_css_map_keys")
    for module, css_pairs in modules:
        for pair in css_pairs():
            key = pair[0]
            default_value = pair[1]
            description = pair[2]
            CSSMap2.register(key, default_value, description)
