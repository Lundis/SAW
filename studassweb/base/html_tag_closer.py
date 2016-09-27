# coding=utf-8
from html.parser import HTMLParser
import re
import logging

IGNORED_TAGS = ("img",)

logger = logging.getLogger(__name__)


class HTMLTagCloser(HTMLParser):
    active_tags = []

    def handle_starttag(self, tag, attrs):
        """

        :param tag:
        :param attrs:
        """
        if tag not in IGNORED_TAGS:
            self.active_tags.append(tag)

    def handle_endtag(self, tag):
        """

        :param tag:
        """
        if tag not in IGNORED_TAGS:
            # remove the top-most tag from active_tags if it matches
            if self.active_tags[-1] == tag:
                self.active_tags.pop()
            else:
                # we have invalid html and need to close a tag in the middle of the text
                logger.debug("invalid html detected. tag: " + tag)

    def handle_startendtag(self, tag, attrs):
        """

        :param tag:
        :param attrs:
        """
        pass

    def get_end_of_string(self):
        """

        :return:
        """
        end = ""
        for tag in reversed(self.active_tags):
            end += "</%s>" % tag
        return end


def complete_html(html):
    """
    Analyzes the given string and returns a string where any unclosed tags are closed at the end
    :param html:
    :return:
    """
    # make sure that the html isn't cut off in the middle of a tag
    match = re.search("(<[^>]+)$", html)
    if match:
        # if it is, remove the entire last unfinished tag
        html = html[:match.start()]
    parser = HTMLTagCloser()
    parser.feed(html)
    return html, parser.get_end_of_string()


