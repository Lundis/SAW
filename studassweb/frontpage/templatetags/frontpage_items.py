from django import template

register = template.Library()


@register.inclusion_tag("frontpage/item.html", takes_context=True)
def display_frontpage_item(context, item, edit_mode, placement):
    if placement not in ("main", "side", "hidden"):
        raise ValueError("Invalid placement: %s" % placement)
    content = item.render_content(context)
    return {'item': item,
            'content': content,
            'edit_mode': edit_mode,
            'placement': placement}