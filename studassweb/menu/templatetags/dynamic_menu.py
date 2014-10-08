from django import template

register = template.Library()

@register.tag()
def display_menu(parser, token):
    try:
        # token.split_contents() takes into account quotes
        tag_name, menu, active_tab = token.split_contents()
    except:
        raise template.TemplateSyntaxError("%r tag requires two arguments: menu name and active item" % token.contents.split()[0])
    if not (is_in_quotes(menu) and is_in_quotes(active_tab)):
        raise template.TemplateSyntaxError("%r tag's arguments should be in quotes" % tag_name)

    return DynamicMenu(menu, active_tab)

def is_in_quotes(s):
    return s[0] == s[-1] and s[0] in ('"', "'")

class DynamicMenu(template.Node):
    def __init__(self, menu, active):
        """
        :param active: the name of the active "tab"
        :return:
        """
        self.menu = menu
        self.active = active

    def render(self, context):
        """
        :param context:
        :return: a string containing the entire menu HTML
        """
        # TODO: add the active tab to context
        context['active_tab'] = self.active
        # load template file
        template_text = template.get_template("menu/menu.html")
        # create a template
        menu_template = template.Template(template_text)
        return menu_template.render(context)