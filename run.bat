@echo off
cd /d D:\Organization

call venv\Scripts\activate

python manage.py migrate --noinput

waitress-serve ^
  --host=127.0.0.1 ^
  --port=8005 ^
  Organization.wsgi:application
