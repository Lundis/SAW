from django.template import RequestContext, Library
from ..models import InstallProgress

register = Library()


@register.inclusion_tag('install/progress_bar.html', takes_context=True)
def display_progress_bar(context, active_tab):
    """
    Renders the installation wizard's progress bar
    :param active_tab: The active installation phase
    :return:
    """
    progress, created = InstallProgress.objects.get_or_create()

    return {'progress': progress, 'active_tab': active_tab, 'user': context['user']}
