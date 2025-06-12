#!/bin/bash

nginx -g 'daemon on;'
gunicorn --bind 0.0.0.0:3000 --timeout 1000 --workers 4 --max-requests 1000 api:'create_app()'
