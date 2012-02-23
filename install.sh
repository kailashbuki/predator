#!/bin/sh

mkdir -p /opt/predator
export PREDATOR_HOME=/opt/predator

# Move all files into PREDATOR_HOME directory
echo "copying all files into /opt/predator"
cp -r * "$PREDATOR_HOME"

# make symbolic link to nginx service
echo 'creating a symbolic link to nginx service'
ln -s "$PREDATOR_HOME"/installed/webserver/deploy/nginx_service "$PREDATOR_HOME"/etc/services/nginx

# make directories for storage
mkdir -p "$PREDATOR_HOME"/volumes/predator/db
mkdir -p "$PREDATOR_HOME"/volumes/predator/files

# make directory for temporary uploading
mkdir -p /tmp/queue

# make directories for log files
echo 'making log directories'
mkdir -p "$PREDATOR_HOME"/var/log/nginx
mkdir -p "$PREDATOR_HOME"/var/log/services/nginx
mkdir -p "$PREDATOR_HOME"/var/log/services/gunicorn
mkdir -p "$PREDATOR_HOME"/var/log/services/agentfront
mkdir -p "$PREDATOR_HOME"/var/log/services/pdf2textconverter
mkdir -p "$PREDATOR_HOME"/var/log/services/sanitizer
mkdir -p "$PREDATOR_HOME"/var/log/services/fpkeeper
mkdir -p "$PREDATOR_HOME"/var/log/services/comparator

# start mongodb and add the user into the db
mongodb_lockfile="$PREDATOR_HOME/volumes/predator/db/mongod.lock"
if [ -f "$mongodb_lockfile" ] ; then
        echo "MongoDB is already running"
else
        echo "Starting mongodb in daemon mode"
        mongod --fork --logpath "$PREDATOR_HOME"/var/log/mongodb.log --logappend --port 27017 --dbpath "$PREDATOR_HOME"/volumes/predator/db/
fi

echo 'preparing database for the first run; adding user'
sudo "$PREDATOR_HOME"/bin/update_db.py

# start all services
echo "starting all services"
exec "$PREDATOR_HOME"/bin/start_predator