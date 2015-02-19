from django.template import Library
from django.template.smartif import IfParser, Literal
from django.template.base import (
    BLOCK_TAG_END, BLOCK_TAG_START, COMMENT_TAG_END, COMMENT_TAG_START,
    SINGLE_BRACE_END, SINGLE_BRACE_START, VARIABLE_ATTRIBUTE_SEPARATOR,
    VARIABLE_TAG_END, VARIABLE_TAG_START, Context, InvalidTemplateLibrary,
    Library, Node, NodeList, Template, TemplateSyntaxError,
    VariableDoesNotExist, get_library, kwarg_re, render_value_in_context,
    token_kwargs,
)
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

    # Not sure if we should implement this? And what it is supposed to do
    def __iter__(self):
        print("hit the mysterious __iter__")
        for node in self.nodelist_header:
            yield node
        for node in self.nodelist_body:
            yield node

    # context_ should maybe be in context?
    def render(self, context):
        if self.nodelist_body:  # Print with template
            context_ = Context({'title': self.nodelist_header.render(context),
                                'body': self.nodelist_body.render(context)})
            # context['title'] = self.nodelist_header.render(context)
            # context.push
            # context['body'] = self.nodelist_body.render(context)
            # context.push()
            template_ = get_template(PANEL_TEMPLATE_PRE + self.template_name.resolve(context) + PANEL_TEMPLATE_POST)
            return template_.render(context_)
        else:                   # Empty panel
            return ""


@register.tag('sidebarpanel')
def do_panel(parser, token):
    """
    23:55 <MaQ> we need a turbosolutiontemplatetag!
    23:56 <ld-s> hm hu sku man tro lag he..
    23:57 <ld-s> iofs man kan lag just na tådde som tar block som argument (som if å for jer)
    23:57 <MaQ> jo precis na tåli
    23:57 <ld-s> å så använder man täj iställe fö panel4-title å panel4-body
    23:57 <ld-s> så använder man bara sidebar-panel4 blocke
    23:59 <ld-s> {{if show_shit }} {% panel %} "my title" {% body %} "random buttons {%endpanel %}
    23:59 <ld-s> he bord väl lös probleme?
    Day changed to 19 Feb 2015
    00:00 <MaQ> joh, he låter no bra
    00:02 <ld-s> ska ja lag a elå?
    00:03 <MaQ> nå ja tänkt ga ligg nu, men ja kan no si på a imorron
    00:03 <ld-s> yees, ja vill minnas att docsen rekommendera att man kolla på hu if-else va implementera i django-srcen
    00:03 <MaQ> jepps
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
