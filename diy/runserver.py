
from app import application

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
http_server = WSGIServer(('127.9.114.1',8080), application, handler_class=WebSocketHandler)
http_server.serve_forever()
