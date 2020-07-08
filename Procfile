release: python pyforum/manage.py migrate
web: gunicorn -c pyforum config.wsgi --log-file -
