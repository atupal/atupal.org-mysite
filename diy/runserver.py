
from application import app

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
app.config.from_envvar('PY27_ATUPAL_ORG_CONFIG')

if __name__ == "__main__":
    http_server = WSGIServer(('127.9.114.1', 8080), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
