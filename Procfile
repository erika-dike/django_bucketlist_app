web: python bucketlist/manage.py collectstatic --noinput --settings=bucketlist.settings.production --verbosity 0; gunicorn bucketlist.wsgi --pythonpath=bucketlist --log-file -