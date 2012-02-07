#!/bin/sh

mkdir -p /opt/predator
export PREDATOR_HOME=/opt/predator

# Move all files into PREDATOR_HOME directory
echo "copying all files into /opt/predator"
cp -r * "$PREDATOR_HOME"

# copy the disc/etc/env.rc into ~/.profile
echo "appending the envionment variables to ~/.profile"
cat "$PREDATOR_HOME"/etc/env.rc >>~/.profile

# make symbolic link to nginx service
ln -s "$PREDATOR_HOME"/installed/webserver/deploy/nginx_service "$PREDATOR_HOME"/etc/services/nginx

# make directories for storage
mkdir -p "$PREDATOR_HOME"/volumes/predator/db
mkdir -p "$PREDATOR_HOME"/volumes/predator/files

# make directory for temporary uploading
mkdir -p /tmp/queue

# make directories for log files
mkdir -p "$PREDATOR_HOME"/var/log/nginx
mkdir -p "$PREDATOR_HOME"/var/log/services/nginx
mkdir -p "$PREDATOR_HOME"/var/log/services/gunicorn
mkdir -p "$PREDATOR_HOME"/var/log/services/agentfront
mkdir -p "$PREDATOR_HOME"/var/log/services/pdf2textconverter
mkdir -p "$PREDATOR_HOME"/var/log/services/sanitizer
mkdir -p "$PREDATOR_HOME"/var/log/services/fpkeeper
mkdir -p "$PREDATOR_HOME"/var/log/services/comparator

# start all services
echo "starting all services"
exec "$PREDATOR_HOME"/bin/start_predator
