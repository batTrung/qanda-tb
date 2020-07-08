release: python pyforum/manage.py migrate
web: gunicorn --pythonpath pyforum/config.wsgi --log-file -
heroku ps:scale web=1
