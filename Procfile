release: python manage.py migrate && python manage.py compilemessages -l uk
web: gunicorn py_june.wsgi --log-file -
