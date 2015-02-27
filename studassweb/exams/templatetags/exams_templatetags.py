from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def can_edit_course(context, course):
    return course.user_can_edit(context['request'].user)


@register.assignment_tag(takes_context=True)
def can_edit_examinator(context, examinator):
    return examinator.user_can_edit(context['request'].user)


@register.assignment_tag(takes_context=True)
def can_edit_exam(context, exam):
    return exam.user_can_edit(context['request'].user)