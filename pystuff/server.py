import logging
from socketserver import BaseRequestHandler, TCPServer
import time

from .request import HttpRequest
from .response import Response

class IllegalArgument(Exception):
    pass


def require(arg, msg):
    if arg is None:
        raise IllegalArgument(msg)
    return arg


def read_request(conn, buffer_size=4096):
    return HttpRequest(conn.recv(buffer_size).decode().strip())


class Dispatcher(BaseRequestHandler):
    def handle(self):
        req = read_request(self.request)
        logging.info("[id - %s] received %s request to %s at %d",
                req.id, req.verb, req.path, int(time.time()))

        _handle = self.server.router.get_handler(req)

        try:
            response = _handle(req)
        except Exception as e:
            response = Response(500)

        try:
            logging.info("[id - %s] response status %s at %d",
                    req.id, response.status, int(time.time()))
            self.request.sendall(response.bytes)
        except Exception as e:
            logging.error("[id - %s] error sending response %s at %d",
                    req.id, e, int(time.time()))
            self.request.close()


class Server(object):
    def __init__(self, host='localhost', port=8080, router=None):
        self.host = require(host, 'host')
        self.port = require(port, 'port')
        self.router = require(router, 'router')

    def run(self):
        with TCPServer((self.host, self.port), Dispatcher) as server:
            server.router = self.router
            server.serve_forever()
