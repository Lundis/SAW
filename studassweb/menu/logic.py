from django.conf import settings

def find_modules():
    """ Checks if any new modules have been added, and if so, updates the database.
        Should be called whenever you add or remove a module.
    """
    #TODO: figure out if the modules should be fetched form settings.INSTALLED_APPS instead of a directory listing

    #TODO: list all folders in settings.BASE_DIR
    #TODO: check which ones have a urls.py and does not contain settings.py (ignore project folder),
    #  also attempt to import the folders as modules and ignore unloadable ones
    #TODO: check if they actually are in settings.INSTALLED_APPS, otherwise they cant be used

    #TODO: load the menu table from the database and see if anything has changed
    #TODO: if it has, update it
    pass

def refresh_menu():
	"""
	  Should be ran after stuff have been reordered, added or removed from the menu.
	"""

	pass