# coding=utf-8
from django.test import TestCase

from base.html_tag_closer import complete_html


class HtmlTagCompleterTest(TestCase):

    def test1(self):
        with open('base/test.html') as content_file:
            content = content_file.read().strip()
            completed, end = complete_html(content)
            if end != "":
                print(completed)
                print(end)
                self.fail("correct html was completed")


