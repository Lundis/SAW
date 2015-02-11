from django.template import Library
from base.models import SiteConfiguration, Feedback
import random
import logging

register = Library()

logger = logging.getLogger(__name__)


@register.inclusion_tag('base/tags/helptext_feedback.html', takes_context=True)
def helptext_feedback(context):
    config = SiteConfiguration.instance()
    template_context = {}
    request = context['request']
    if config.show_feedback_helptext:
        if Feedback.can_user_give_feedback(ip=request.META['REMOTE_ADDR'],
                                           type=Feedback.FEEDBACK_HELPTEXT,
                                           url=request.path,
                                           user=request.user):
            template_context['response_yes'] = Feedback.RESPONSE_GOOD
            template_context['response_no'] = Feedback.RESPONSE_BAD
            template_context['response_unnecessary'] = Feedback.RESPONSE_UNNECESSARY
            template_context['id'] = str(random.randint(1, 10000000))
            template_context['url'] = request.path
    return template_context