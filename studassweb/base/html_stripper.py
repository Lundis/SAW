from html.parser import HTMLParser

import logging

logger = logging.getLogger(__name__)


class _HTMLStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_html(html: str) -> str:
    """
    Analyzes the given string and returns a string where any unclosed tags are closed at the end
    :param html:
    :return:
    """
    parser = _HTMLStripper()
    parser.feed(html)
    return parser.get_data()


