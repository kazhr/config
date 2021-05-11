#!/bin/sh

# adminユーザー
email=root@localhost
user=admin
pass=admin

# initialize db
if [ ! -e db.sqlite3 ]; then
  python manage.py migrate
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$user', '$email', '$pass')"| python manage.py shell
fi

# update static files
python manage.py collectstatic --no-input

# updaste db
python manage.py migrate

# run
gunicorn myproject.wsgi --bind=0.0.0.0:8000
