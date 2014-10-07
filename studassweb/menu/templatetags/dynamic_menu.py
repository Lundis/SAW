from django import template

register = template.Library()

@register.tag()
def display_menu(parser, token):
    try:
        tag_name, active_tab = token.split_contents()
    except:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (active_tab[0] == active_tab[-1] and active_tab[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)

    return DynamicMenu(active_tab)


class DynamicMenu(template.Node):
    def __init__(self, active):
        """
        :param active: the name of the active "tab"
        :return:
        """
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