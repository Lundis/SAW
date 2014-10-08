from django.conf import settings
import os

def find_apps():
    """ Checks if any apps have been added/removed, and if so, updates the database.
        Must be called whenever you add or remove a module that can show up in the menu.
    """
    menu_apps = ()
    apps_in_base_dir = os.listdir(settings.BASE_DIR)
    for app in settings.INSTALLED_APPS:
        # is the app one of our apps (not Django's builtin)?
        if app in apps_in_base_dir:
            # check if the app has a urls.py file, i.e. if it has something to show
            app_path = os.path.join(settings.BASE_DIR, app)
            url_file = os.path.join(app_path, "urls.py")
            if os.path.isfile(url_file):
                # TODO: add a final test that checks if there is an entry in the url file for r'^$' ?
                #       This is to ensure that it doesn't 404 when we access it by "host/app"
                menu_apps += (app, )
    #Ok, now we have all the possible apps that the menu can display
    #TODO: load the menu table from the database and see if anything has changed
    #TODO: if it has, update it
    pass

def refresh_menu():
	"""
	  Should be ran after stuff have been reordered, added or removed from the menu.
	"""

	pass