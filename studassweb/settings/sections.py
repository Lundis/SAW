from base.utils import get_modules_with
from users.permissions import has_user_perm


class Section:

    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description
        self.pages = ()

    def can_view(self, user):
        """
        Returns true if the user can view any of the pages in this section
        :param user:
        :return:
        """
        for page in self.pages:
            if has_user_perm(user, page.permission):
                return True
        return False

    def pages(self):
        """
        Returns the pages in this section
        :return:
        """
        return self.pages

    def populate(self, pages):
        self.pages = Page.filter_for_section(pages, self.id)

    @staticmethod
    def _get_sections():
        sections = STANDARD_SECTIONS
        mod_funcs = get_modules_with("register", "register_sections")
        existing_ids = [obj.id for obj in sections]
        for mod, section_func in mod_funcs:
            section = section_func()
            if section.id not in existing_ids:
                sections += (section,)
                existing_ids.append(section.id)
        return sections

    @staticmethod
    def get_all_sections():
        sections = Section._get_sections()
        pages = Page.get_all_pages()
        for section in sections:
            section.populate(pages)
        return sections

    @staticmethod
    def get_section(section_id):
        sections = Section._get_sections()
        pages = Page.get_all_pages()
        for section in sections:
            if section.id == section_id:
                section.populate(pages)
                return section


class Page:

    def __init__(self, title, section_id, url, permission):
        self.title = title
        self.section_id = section_id
        self.url = url
        self.permission = permission

    def can_view(self, user):
        return not self.permission or has_user_perm(user, self.permission)

    @staticmethod
    def get_all_pages():
        pages = ()
        mod_funcs = get_modules_with("register", "register_settings_pages")
        for mod, func in mod_funcs:
            pages_from_mod = func()
            pages += (pages_from_mod,)
        return pages

    @staticmethod
    def filter_for_section(pages, section):
        return [p for p in pages if p.section_id == section.id]

SECTION_PERSONAL_SETTINGS = "personal"
SECTION_LAYOUT = "layout"
SECTION_ADVANCED = "advanced"

STANDARD_SECTIONS = (
    Section(SECTION_PERSONAL_SETTINGS, "Personal", "Personal settings"),
    Section(SECTION_LAYOUT, "Theme and Layout", "Personal settings"),
    Section(SECTION_ADVANCED, "Advanced", "Personal settings"),
)

