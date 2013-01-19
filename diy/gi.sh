#!/bin/bash
#uwsgi -s 127.0.0.1:5000 --socket-protocol http --pp ./ --module application --pidfile ~/tmp/uwsgi.pid

#python application.py

uwsgi -s /tmp/uwsgi.sock --pp ./ --module application --chmod-socket 666
