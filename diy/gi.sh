#!/bin/bash
#uwsgi -s 127.0.0.1:5000 --socket-protocol http --pp ./ --module application --pidfile ~/tmp/uwsgi.pid

#python application.py
export PY27_ATUPAL_ORG_CONFIG=/home/atupal/.config/myapp/py27_config.ini
uwsgi -s /tmp/uwsgi.sock --pp ./ --module runserver:app --chmod-socket 666
