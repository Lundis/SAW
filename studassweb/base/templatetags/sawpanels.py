# coding=utf-8
from django.template.base import Context, Node
from django import template
from django.template.loader import get_template
from django.template.base import kwarg_re
from string import ascii_letters, digits

__author__ = 'Lundis'
# Based on Magnus' similar sidemenu.py

register = template.Library()

PANEL_PRE = "base/sawpanels/"
DEFAULT_PANEL_TEMPLATE = "\"primary\""
PANEL_TEMPLATE_POST = ".html"


class PanelNode(Node):
    """
    This node represents a panel with header, body and footer
    """
    child_nodelists = ('nodelist_header', 'nodelist_body', 'nodelist_footer')

    def __init__(self, template_name, nodelist_header, nodelist_body, nodelist_footer, kwargs, args):
        self.template_name = template.Variable(template_name)
        self.nodelist_header = nodelist_header
        self.nodelist_body = nodelist_body
        self.nodelist_footer = nodelist_footer
        self.kwargs = kwargs
        self.args = args

    def __repr__(self):
        return "<PanelNode>"

    def render(self, context):
        """

        :param context:
        :return:
        """
        panel_attrs = ""
        for name, value in self.kwargs:
            panel_attrs += " " + name + "=" + template.Variable(value).render(context)
        for arg in self.args:
            panel_attrs += " " + arg
        if self.nodelist_footer is None:
            footer = None
        else:
            footer = self.nodelist_footer.render(context)

        context_ = Context({'title': self.nodelist_header.render(context),
                            'body': self.nodelist_body.render(context),
                            'footer': footer,
                            'attrs': panel_attrs
                            })
        template_name = self.template_name.resolve(context)
        # We want to avoid ../../ bullshit
        if all(c in ascii_letters + digits + '-' + '_' for c in template_name):
            template_ = get_template(PANEL_PRE + self.template_name.resolve(context) + PANEL_TEMPLATE_POST)
            return template_.render(context_)
        else:
            raise ValueError("Template name only allows alphanumeric-_ chars ")


@register.tag('sawpanel')
def sawpanel(parser, token):
    """
    This tag outputs the html for a sidemenu panel.
    Example:

    {% sawpanel "primary" kw1="arg1" kw2="arg2" %}
        This is title of panel
        {% body %}
        This is the body of the panel
        {% footer %}
        This is the body of the footer
    {% endpanel %}

    results in: (assuming panel-primary is the current primary panel theme)

    <panel class="panel panel-primary" kw1=arg1 kw2=arg2>
        <div class="panel-heading">
            <div class="panel-title">
                {{ title }}
            </div>
        </div>
        <div class="panel-body">
            {{ body }}
        </div>
        <div class="panel-footer">
            {{ footer }}
        </div>
    </panel>


    The argument can be specified as a string or as a variable.

    reference:
      def url(parser, token):
      in django.template.defaulttags
    """

    arguments = token.split_contents()

    if len(arguments) >= 2:
        template_name = arguments[1]
    else:
        template_name = DEFAULT_PANEL_TEMPLATE

    kwargs = {}
    args = []
    # parse keyword arguments
    if len(arguments) >= 3:
        for bit in arguments[2:]:
            match = kwarg_re.match(bit)
            if not match:
                raise template.TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)

    # parse until one of the keywords
    nodelist_header = parser.parse(('body', 'footer', 'endsawpanel'))

    # handle the body
    token = parser.next_token()
    assert token.contents == 'body'
    nodelist_body = parser.parse(('footer', 'endsawpanel'))

    # handle the footer
    token = parser.next_token()
    if token.contents == 'footer':
        nodelist_footer = parser.parse(('endsawpanel',))
        token = parser.next_token()
    else:
        nodelist_footer = None

    assert token.contents == "endsawpanel"
    return PanelNode(template_name, nodelist_header, nodelist_body, nodelist_footer, kwargs, args)
