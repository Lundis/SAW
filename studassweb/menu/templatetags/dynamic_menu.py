from django.template import RequestContext, Library
from django.template.loader import get_template
from menu.models import MenuTemplate, Menu

register = Library()


@register.inclusion_tag('menu/menus/menu_placeholder.html', takes_context=True)
def display_menu(context, menu_name, active_tab):
    menu = render_menu(menu_name, active_tab, context)
    return {'menu': menu}


def render_menu(menu_name, active_tab, http_context):
    menu = Menu.get(menu_name)
    context = {'menuitems': menu.items(http_context['user']), 'active_tab': active_tab}

    if menu.template and menu.template.path:
        template_path = menu.template.path
    else:
        raise ValueError("You cannot render a menu without a template using display_menu")

    template = get_template(template_path)
    request_context = RequestContext(http_context, context)
    request_context['user'] = http_context['user']
    result = template.render(request_context)
    return result


@register.inclusion_tag('menu/menus/login_menu.html', takes_context=True)
def display_login_button(context):
    items = Menu.get("login_menu").items(context['user'])
    return {'menuitems': items, 'user': context['user']}
