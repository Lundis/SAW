from django.template import Context, Template, Library, TemplateSyntaxError, Node
from django.template.loader import get_template
from menu.models import MenuTemplate, Menu

register = Library()

@register.simple_tag
def display_menu(menu_name, active_tab):
    menu = Menu.objects.get(menu_name=menu_name)
    context = Context({'menuitems': menu.items(),
                       'active_tab': active_tab})
    template_path = MenuTemplate.default().path
    if menu.template and menu.template.path != "":
        template_path = menu.template.path
    template = get_template(template_path)
    result = template.render(context)
    return result
