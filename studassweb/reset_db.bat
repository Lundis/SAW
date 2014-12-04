@echo off

REM delete db
del db.sqlite3

REM since del is not returning an errorlevel (WTF!!1!)
REM check manually if file was actually removed or go to end
@dir db.sqlite3 >NUL 2>&1 && goto :eof

REM do django stuff
python manage.py makemigrations && ^
python manage.py migrate && ^
python manage.py createsuperuser && ^
python manage.py runserver 
pause