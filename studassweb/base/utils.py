import os
from django.conf import settings
from inspect import isfunction

def get_modules_with(file_name, function_name):
    """
    :param file_name: filename (without .py ending) that must be in the module
    :param function_name: function that must be in the file. None if you're just looking for the file
    :return: a tuple of module identifiers that have the specified file and function
    """
    modules = ()
    modules_in_base_dir = os.listdir(settings.BASE_DIR)
    for module in modules_in_base_dir:
        # is it a python module?
        if os.path.isfile(os.path.join(module, "__init__.py")):
            if file_name == None:
                modules += (module, )
                continue
            # check if the file exists in this module
            app_path = os.path.join(settings.BASE_DIR, module)
            file_path = os.path.join(app_path, file_name + ".py")
            if os.path.isfile(file_path):
                if function_name == None:
                    modules += (module, )
                    continue

                # now load the module
                try:
                    mod = __import__(module)
                    file = getattr(mod, file_name)
                    # is there anything with the right name in the file?
                    if hasattr(file, function_name):
                        # is it an actual function or just a variable?
                        f = getattr(file, function_name)
                        if isfunction(f):
                            modules += (module, )
                except:
                    # ignore modules with errors.
                    #TODO: log the error
                    pass
    return modules

def get_all_modules():
    return get_modules_with(None, None)