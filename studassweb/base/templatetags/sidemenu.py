from django.template.base import (Context, Library, Node)
from django import template
from django.template.loader import get_template


register = Library()
PANEL_TEMPLATE_PRE = "base/sidemenu/sidemenupanel_"
DEFAULT_PANEL_TEMPLATE = "\"vertical_buttons\""
PANEL_TEMPLATE_POST = ".html"


class PanelNode(Node):
    child_nodelists = ('nodelist_header', 'nodelist_body')

    def __init__(self, template_name, nodelist_header, nodelist_body):
        self.template_name = template.Variable(template_name)
        self.nodelist_header = nodelist_header
        self.nodelist_body = nodelist_body

    def __repr__(self):
        return "<PanelNode>"

    def render(self, context):
        if self.nodelist_body:  # Print with template
            context_ = Context({'title': self.nodelist_header.render(context),
                                'body': self.nodelist_body.render(context)})
            template_ = get_template(PANEL_TEMPLATE_PRE + self.template_name.resolve(context) + PANEL_TEMPLATE_POST)
            return template_.render(context_)
        else:                   # Empty panel
            return ""


@register.tag('sidebarpanel')
def do_panel(parser, token):
    """
    This tag outputs the html for a sidemenu panel.
    Example:

    {% sidebarpanel %}
        This is title of panel
        {% body %}
        This is the body of the panel
    {% endsidebarpanel %}

    The template for the html can be chosen dynamically with the first argument.
    Example:
    {% block sidebar-panel-help %}
        {% sidebarpanel "help" %}
            {% trans "Help" %}
            {% body %}
            <p>{% trans "Press button for perjantai" %}</p>
        {% endsidebarpanel %}
    {% endblock %}

    The argument can be specified as a string or as a variable.

    If no {% body %} tag is found the whole panel tag returns nothing. This is in hindsight completely unneccessary.
    """

    # contents is the arguments for the block
    contents = token.split_contents()
    if len(contents) >= 2:
        template_name = contents[1]
    else:
        template_name = DEFAULT_PANEL_TEMPLATE

    nodelist_header = parser.parse(('body', 'endsidebarpanel'))

    token = parser.next_token()

    # should handle the body
    if token.contents == 'body':
        nodelist_body = parser.parse(('endsidebarpanel',))
    else:
        # There is no {% body %}, this is a empty panel!
        nodelist_body = None

    token = parser.next_token()

    # {% endif %}
    assert token.contents == 'endsidebarpanel'

    return PanelNode(template_name, nodelist_header, nodelist_body)
