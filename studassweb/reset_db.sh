#!/bin/bash
if ! [ -e ./manage.py ]
then
    # print to stderr
    >&2 echo "You are not in the right directory. Please go to the directory with manage.py!"
    return 1
fi

if ! [ -e ./studassweb/settings_local.py ]
then
    cp ./studassweb/settings_local.py.template ./studassweb/settings_local.py
fi

rm -f db.sqlite3 && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py createsuperuser && python3 manage.py runserver