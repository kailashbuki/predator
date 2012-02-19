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
wget http://cloud.github.com/downloads/libevent/libevent/libevent-2.0.17-stable.tar.gz
echo 'installing libevent'
tar -C /tmp -xzf /tmp/libevent-2.0.17-stable.tar.gz
cd /tmp/libevent-2.0.17-stable
./configure
make
sudo make install

echo 'Downloading & installing gevent'
sudo pip install gevent

echo 'Downloading gunicorn'
sudo pip install gunicorn

cd /tmp
echo 'Downloading nginx'
wget http://nginx.org/download/nginx-1.0.12.tar.gz
echo 'Installing nginx'
tar -C /tmp -xzf /tmp/nginx-1.0.12.tar.gz
cd /tmp/nginx-1.0.12
./configure
make
sudo make install

cd /tmp
echo 'Installing libtool, autoconf, automake'
sudo apt-get install libtool autoconf automake

echo 'Installing  uuid-dev package, uuid/e2fsprogs'
sudo apt-get install uuid-dev package uuid/e2fsprogs

echo 'Downloading zeromq'
wget http://download.zeromq.org/zeromq-2.1.11.tar.gz
echo 'Installing zeromq'
tar -C /tmp -xzf /tmp/zeromq-2.1.11.tar.gz
cd /tmp/zeromq-2.1.11
./configure
make
sudo make install
sudo ldconfig

echo 'Downloading pyzmq'
sudo pip install pyzmq

cd /tmp
echo 'Downloading xz utils'
wget http://tukaani.org/xz/xz-5.0.3.tar.gz
echo 'Installing xz utils'
tar -C /tmp -xzf /tmp/xz-5.0.3.tar.gz
cd /tmp/xz-5.0.3
./configure
make
sudo make install

cd /tmp
echo 'Downloading libpng'
wget ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng-1.5.8.tar.xz
echo 'Installing libpng'
xz -d /tmp/libpng-1.5.8.tar.xz
tar -xzf libpng-1.5.8.tar
cd /tmp/libpng-1.5.8
./configure
make
sudo make install

cd /tmp
echo 'Downloading libpoppler'
wget http://poppler.freedesktop.org/poppler-0.18.4.tar.gz
echo 'Installing libpoppler'
tar -C /tmp -xzf /tmp/poppler-0.18.4.tar.gz
cd /tmp/poppler-0.18.4
./configure
make
sudo make install

cd /tmp
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