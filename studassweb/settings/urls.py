from django.conf.urls import patterns, url, include
from menu.models import Menu
urlpatterns = patterns('',
    url(r'^$', 'settings.views.main', name='settings_main'),
)

# Here comes the tricky part. We will get the possible settings URLs by looking at the URLs of the menu items.

# At this point the settings menu has been set up. If not, something is very wrong and this will fail.
modules = ()
for menu_item in Menu.get_or_none("settings_menu").items():
    module = menu_item.app_name
    # Make sure that we only add each module once.
    if module not in modules:
        pattern = "^" + module + "/"
        settings_url = module + ".settings_pages"
        urlpatterns += (
            url(pattern, include(settings_url)),
        )
        modules += (module,)