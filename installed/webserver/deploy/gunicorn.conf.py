#!/usr/bin/env python

import multiprocessing

bind = "127.0.0.1:6969"
workers = multiprocessing.cpu_count() * 2 + 1
preload = True
worker_class = "gevent"
loglevel = "debug"
