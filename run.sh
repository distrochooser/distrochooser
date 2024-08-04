#!/bin/bash

# Copy the precompiled assets

cp -v /kuusi/static-buildtime/* /kuusi/static/

python manage.py migrate

gunicorn kuusi.wsgi --timeout 600 -b 0.0.0.0