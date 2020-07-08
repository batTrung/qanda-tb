release: python pyforum/manage.py migrate
web: gunicorn --chdir pyforum/ config.wsgi --log-file -
