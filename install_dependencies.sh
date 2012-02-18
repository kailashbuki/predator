#!/usr/bin/sh

sudo mkdir -p /tmp

cd /tmp

echo 'Installing curl first'
sudo apt-get install curl

echo 'Downloading & installing python development headers'
sudo apt-get install python-dev

echo 'Downloading & installing distribute'
sudo curl http://python-distribute.org/distribute_setup.py | sudo python

echo 'Downloading libevent'
wget https://github.com/downloads/libevent/libevent/libevent-2.0.17-stable.tar.gz
echo 'installing libevent'
tar -C /tmp -xzf /tmp/libevent-2.0.17-stable.tar.gz
cd /tmp/libevent-20.17
./configure
make
sudo make install

echo 'Downloading & installing gevent'
sudo pip install gevent

echo 'Downloading gunicorn'
sudo pip install gunicorn

echo 'Downloading nginx'
sudo pip install nginx

echo 'Downloading zeromq'
wget http://download.zeromq.org/zeromq-2.1.11.tar.gz
echo 'Installing zeromq'
tar -C /tmp -xzf /tmp/zeromq-2.1.11.tar.gz
cd /tmp/zeromq-2.1.11
./configure
make
sudo make install

echo 'Downloading pyzmq'
sudo pip install pyzmq

echo 'Downloading libpng'
wget http://downloads.sourceforge.net/project/libpng/libpng15/older-releases/1.5.7/libpng-1.5.7.tar.xz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Flibpng%2Ffiles%2F&ts=1329403713&use_mirror=space
echo 'Installing libpng'
tar -C /tmp -xzf /tmp/libpng-1.5.7.tar.xz
cd /tmp/libpng-1.5.7
./configure
make
sudo make install

echo 'Downloading libpoppler'
wget http://poppler.freedesktop.org/poppler-0.18.4.tar.gz
echo 'Installing libpoppler'
tar -C /tmp -xzf /tmp/poppler-0.18.4.tar.gz
cd /tmp/poppler-0.18.4
./configure
make
sudo make install

echo 'Downloading mongodb 64-bit'
wget http://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.0.2.tgz
echo 'Installing mongodb'
tar -C /tmp -xzf /tmp/mongodb-linux-x86_64-2.0.2.tgz
cd /tmp/mongodb-linux-x86_64-2.0.2
./configure
make
sudo make install

echo 'Downloading pymongo'
sudo pip install pymongo

echo 'Downloading mongokit'
sudo pip install mongokit

echo 'Downloading flask'
sudo pip install flask

echo 'Downloading werkzeug'
sudo pip install werkzeug

echo 'Downloading jinja2'
sudo pip install jinja2

echo 'Downloading wtform-fork'
sudo pip install hg + https://bitbucket.org/kailashbuki/wtforms-fork
