release: python manage.py migrate && python manage.py compilemessages
web: gunicorn py_june.wsgi --log-file -
