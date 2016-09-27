# coding=utf-8


class InfoFrontPageItem:

    def __init__(self, page):
        self.page = page

    def title(self):
        return self.page.title

    def contents(self):
        return self.page.text

    @staticmethod
    def show_in_side_bar():
        return True

    @staticmethod
    def show_in_main_bar():
        return True
