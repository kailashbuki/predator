#!/bin/sh

export PREDATOR_HOME="/opt/predator"
cd "$PREDATOR_HOME"/installed/webserver 
exec gunicorn -c "$PREDATOR_HOME"/installed/webserver/deploy/gunicorn.conf.py deploy:app "$@"
