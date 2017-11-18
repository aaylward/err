from uuid import uuid4

RN = '\r\n'


def parse_request_string(request_string):
    parts = request_string.split(RN + RN, 1)

    if len(parts) == 2:
        (metadata, body) = parts
    else:
        metadata = parts[0]
        body = None

    (verb_and_path, *headers) = metadata.split(RN)
    (verb, path, protocol) = verb_and_path.split(' ')
    
    return (protocol, path, verb, headers, body)


class HttpRequest(object):
    def __init__(self, data):
        self._id = uuid4()
        (protocol, path, verb, headers, body) = parse_request_string(data)
        self._protocol = protocol
        self._path = path
        self._verb = verb
        self._headers = headers
        self._body = body

    @property
    def id(self):
        return self._id

    def resource(self):
        return frozenset({'path': self._path, 'verb': self._verb})

    @property
    def verb(self):
        return self._verb

    @property
    def path(self):
        return self._path

    @property
    def protocol(self):
        return self._protocol

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body


def read_request(conn, buffer_size=4096):
    return HttpRequest(conn.recv(buffer_size).decode().strip())
