import os
from django.conf import settings
from inspect import isfunction
from importlib import import_module


def get_modules_with(file_name, function_name):
    """
    :param file_name: filename (without .py ending) that must be in the module. None if you're just looking for modules.
    :param function_name: function that must be in the file. None if you're just looking for the file
    :return: a tuple of tuples (module identifier, function)
    """
    modules = ()
    modules_in_base_dir = os.listdir(settings.BASE_DIR)
    for module in modules_in_base_dir:
        # is it a python module?
        if os.path.isfile(os.path.join(module, "__init__.py")):
            if file_name is None:
                modules += ((module, None),)
                continue
            # check if the file exists in this module
            app_path = os.path.join(settings.BASE_DIR, module)
            file_path = os.path.join(app_path, file_name + ".py")
            if os.path.isfile(file_path):
                if function_name is None:
                    modules += ((module, None), )
                    continue

                # now load the module, the file and get the function.
                f = get_function_from_module(module, file_name, function_name)
                if f is not None:
                    modules += ((module, f), )
                # else catch exception and log error? will fail for now.
                # It shouldn't fail when used correctly. ever.
    return modules


def get_attr_from_module(app, module, attribute, validator):
    """
    :param app: A Django app
    :param module: Python module
    :param attribute:
    :param validator: a boolean function that must evaluate to true for the attribute
    :return:
    """

    mod = import_module(app + "." + module)
    # is there anything with the right name in the file?
    if hasattr(mod, attribute):
        # is it an actual function or just a variable?
        f = getattr(mod, attribute)
        if validator(f):
            return f
    # Otherwise, return None
    return None


def get_function_from_module(app, module, function_name):
    return get_attr_from_module(app, module, function_name, isfunction)


def get_str_from_module(app, module, var_name):
    return get_attr_from_module(app, module, var_name, lambda s: isinstance(s, str))


def get_all_modules():
    return [mod for mod, f in get_modules_with(None, None)]


class IllegalArgumentException(ValueError):
    """
    An exception used when an illegal argument is passed to a function.
    """
    pass