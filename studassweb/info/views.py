from django.shortcuts import render
from users.decorators import has_permission

@has_permission("can_view_public_info_pages")
def main(request):
    """
    renders a list of the different categories. This page shouldn't be used in general, or just for searching purposes.
    :param request:
    :return:
    """
    return render(request, "info/main.html")