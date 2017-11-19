from concurrent.futures import ThreadPoolExecutor
import logging
import socket
import time
from uuid import uuid4

from .request import HttpRequest
from .response import Response


class IllegalArgument(Exception):
    pass


def require(arg, msg):
    if arg is None:
        raise IllegalArgument(msg)
    return arg


def read_request(conn, req_id=None, buffer_size=4096):
    return HttpRequest(conn.recv(buffer_size).decode().strip(), req_id)


def send(conn, response, req_id=None):
    try:
        conn.sendall(response.bytes)
        if response.has_file:
            with open(response.filename, 'rb') as f:
                conn.sendfile(f)
        logging.info("[id - %s] response status %s at %s",
                req_id, response.status, str(time.time()))
    except Exception as e:
        logging.exception("[id - %s] error sending response %s at %s",
                req_id, response, str(time.time()))
    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        finally:
            conn.close()


def try_handle(conn, router):
    req_id = str(uuid4())
    try:
        request = read_request(conn, req_id)
        logging.info("[id - %s] received %s request to %s at %d",
                request.id, request.verb, request.path, int(time.time()))
    except:
        logging.exception("error reading request from %s at %d",
                conn, int(time.time()))
        send(conn, Response(500), req_id)
        return

    try:
        response = router.route(request)
    except Exception as e:
        logging.exception("route handler failed for %s at %d",
                request.resource, int(time.time()))
        response = Response(500)

    send(conn, response, req_id)


class Server(object):
    def __init__(self, host='localhost', port=8080, router=None, executor=None):
        self.host = require(host, 'host')
        self.port = require(port, 'port')
        self.router = require(router, 'router')
        self.executor = executor or ThreadPoolExecutor(max_workers=512)

    def run(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host, self.port))
        serversocket.listen(5)
        print("listening!\n")

        while True:
            (conn, address) = serversocket.accept()
            try:
                self.executor.submit(try_handle, conn, self.router)
            except Exception as e:
                logging.exception("failed to dispatch request from %s at %d",
                        address, int(time.time()))

