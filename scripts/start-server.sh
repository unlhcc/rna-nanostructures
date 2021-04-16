#!/bin/bash

python manage.py migrate
python manage.py load_cms_data rnaNanostructures
exec python manage.py runserver 0.0.0.0:8000
