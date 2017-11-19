import json
import logging
import urllib.parse as urlparse

from .resource import Resource

RN = '\r\n'


def parse_request_string(request_string):
    parts = list(filter(lambda x: len(x.strip()) > 0, request_string.split(RN + RN, 1)))

    if len(parts) == 2:
        (metadata, body) = parts
    elif len(parts) == 1:
        metadata = parts[0]
        body = None
    else:
        raise Exception(locals())

    (verb_and_path, *headers) = metadata.split(RN)
    (verb, path, protocol) = verb_and_path.split(' ')

    if '?' in path:
        (path, qs) = path.split('?', 1)
    else:
        qs = ''
    
    return (protocol, path, urlparse.parse_qs(qs), verb, headers, body)


class HttpRequest(object):
    def __init__(self, data, _id=None):
        self._id = _id
        (protocol, path, qs, verb, headers, body) = parse_request_string(data)
        self._protocol = protocol
        self._path = path.rstrip('/')
        self._query_params = qs
        self._verb = verb.upper()
        self._headers = headers
        try:
            self._body = json.reads(body)
        except Exception:
            self._body = body

    @property
    def id(self):
        return self._id

    @property
    def resource(self):
        return Resource(self._path, self._verb)

    @property
    def verb(self):
        return self._verb

    @property
    def path(self):
        return self._path

    @property
    def qs(self):
        return self._query_params

    @property
    def protocol(self):
        return self._protocol

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

