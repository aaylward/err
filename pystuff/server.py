import logging
from socketserver import BaseRequestHandler, TCPServer
import time

from .request import HttpRequest

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
        response = _handle(req)

        try:
            self.request.sendall(response.bytes)
            logging.info("[id - %s] response status %s at %d",
                    req.id, response.status, int(time.time()))
        except Exception as e:
            logging.error("[id - %s] error %s at %d",
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
