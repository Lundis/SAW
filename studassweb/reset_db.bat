@echo off
REM check if we're in the right directory
IF EXIST .\manage.py (
REM Make sure that there is a local settings file
IF NOT EXIST .\studassweb\settings_local.py (
copy .\studassweb\settings_local.py.template .\studassweb\settings_local.py
)
REM delete db
del db.sqlite3

REM since del is not returning an error level (WTF!!1!)
REM check manually if file was actually removed or go to end
@dir db.sqlite3 >NUL 2>&1 && GOTO :eof

REM do django stuff
python manage.py makemigrations && ^
python manage.py migrate && ^
python manage.py createsuperuser && ^
python manage.py runserver
) ELSE (
ECHO "manage.py not found in current directory!"
EXIT /B 1
)