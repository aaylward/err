import logging
from socketserver import BaseRequestHandler, TCPServer
import time

from .request import HttpRequest
from .router import Router

_router = Router()


def read_request(conn, buffer_size=4096):
    return HttpRequest(conn.recv(buffer_size).decode().strip())


class Dispatcher(BaseRequestHandler):
    def _req_cache(self, conn, holder={'_req': None}):
        if holder['_req'] is None:
            holder['_req'] = read_request(conn)
        return holder['_req']


    @property
    def req(self):
        return self._req_cache(self.request)


    def handle(self):
        logging.info("[id - %s] received %s request to %s at %d",
                self.req.id, self.req.verb, self.req.path, int(time.time()))

        _handle = _router.get_handler(self.req)
        response = _handle(self.req)

        logging.info("[id - %s] response status %s at %d",
                self.req.id, response.status, int(time.time()))

        self.request.sendall(response.bytes)


class Server(object):
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port

    def run(self):
        with TCPServer((self.host, self.port), Dispatcher) as server:
            server.serve_forever()
