import menu.models

SIMPLE_MENU_LAYOUT = "simple menu"
STANDARD_MENU_LAYOUT = "standard menu"
LARGE_MENU_LAYOUT = "large menu"

SIMPLE_MENU_PATH = "menu/menus/simple.html"
STANDARD_MENU_PATH = "menu/menus/standard_menu.html"
LARGE_MENU_PATH = "menu/menus/large_menu.html"

MENU_PATHS = (SIMPLE_MENU_PATH, STANDARD_MENU_PATH, LARGE_MENU_PATH)

PATH_CHOICES = (
    ("simple", SIMPLE_MENU_PATH),
    ("standard", SIMPLE_MENU_PATH),
    ("large", LARGE_MENU_PATH),
)


def setup_menu_module():
    """
    Creates menus and menu templates
    :return:
    """
    simple_template, created = menu.models.MenuTemplate.create(SIMPLE_MENU_LAYOUT,
                                                               SIMPLE_MENU_PATH,
                                                               "A simple menu without a logo",
                                                               False,
                                                               for_main_menu=True)

    standard_template, created = menu.models.MenuTemplate.create(STANDARD_MENU_LAYOUT,
                                                                 STANDARD_MENU_PATH,
                                                                 "A menu with two rows and a small logo",
                                                                 True,
                                                                 for_main_menu=True)

    large_template, created = menu.models.MenuTemplate.create(LARGE_MENU_LAYOUT,
                                                              LARGE_MENU_PATH,
                                                              "A larger menu with a long logo on top",
                                                              True,
                                                              for_main_menu=True)

    main_menu, created = menu.models.Menu.get_or_create("main_menu", standard_template)
    login_menu, created = menu.models.Menu.get_or_create("login_menu")