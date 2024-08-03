#!/bin/bash

# Copy the precompiled assets

# FIXME: URL /static prefix for bootstrap icon fonts properly

cp -v /kuusi/static-buildtime/* /kuusi/static/

python manage.py migrate

gunicorn kuusi.wsgi --timeout 600 -b 0.0.0.0