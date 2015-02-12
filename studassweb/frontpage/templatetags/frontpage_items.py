from django import template

register = template.Library()


@register.inclusion_tag("frontpage/item.html")
def display_frontpage_item(item, edit_mode, placement):
    if placement not in ("main", "side", "hidden"):
        raise ValueError("Invalid placement: %s" % placement)
    return {'item': item,
            'edit_mode': edit_mode,
            'placement': placement}