from django.template import Library
from django.template import TemplateSyntaxError

register = Library()

@register.inclusion_tag('base/page_navigator.html')
def display_navigator(*args):
    if len(args) % 2 != 0:
        raise TemplateSyntaxError("navigator tag requires an even number of arguments")
    context = {'items': []}
    for i in range(int(len(args)/2)):
        url = args[2*i]
        name = args[2*i + 1]
        context['items'] += [{'url': url, 'name': name}]
    return context