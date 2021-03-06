# coding=utf-8
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import get_template
from .models import PagesSettings, InfoPage
from .register import VIEW_BOARD
from frontpage.models import FrontPageItem


def get_started_text():
    context = Context()
    template = get_template("pages/getting_started_template.html")
    return template.render(context)


def setup():
    settings = PagesSettings.instance()
    if not settings.is_setup:

        # create a "get started" info page visible only to board members
        page = InfoPage(title="Getting started",
                        text=get_started_text(),
                        permission=VIEW_BOARD,
                        for_frontpage=True,
                        author=User.objects.all().first())
        page.save()
        # Put it in the main bar on the frontpage
        fp_item = FrontPageItem.get_with_target(page)
        fp_item.location = FrontPageItem.MAINBAR
        fp_item.save()
        # Mark the module as set up
        settings.is_setup = True
        settings.save()
