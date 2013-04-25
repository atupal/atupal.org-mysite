
from application import app

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

import os

if os.environ['HOME'] == '/home/atupal':
    OPENSHIFT_INTERNAL_IP = "127.9.114.1"
    OPENSHIFT_INTERNAL_PORT = 8080
else:
    OPENSHIFT_INTERNAL_IP = os.environ['OPENSHIFT_INTERNAL_IP']
    OPENSHIFT_INTERNAL_PORT = int(os.environ['OPENSHIFT_INTERNAL_PORT'])

app.config.from_envvar('PY27_ATUPAL_ORG_CONFIG')

if __name__ == "__main__":
    http_server = WSGIServer((OPENSHIFT_INTERNAL_IP, OPENSHIFT_INTERNAL_PORT), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
