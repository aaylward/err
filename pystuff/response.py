import collections
from datetime import datetime
import json

RN = '\r\n'

STATUS_MAP = {
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        417: 'Expectation Failed',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        501: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout'
        }


def upcase_keys(map):
    upcased_key_map = {}
    for k, v in map.items():
        upcased_key_map[k.upper()] = v
    return upcased_key_map


class Response(object):
    def __init__(self, status=204, body=None, headers_map=None, default_media_type='application/json; charset=utf-8'):
        self._status = status
        self._body = body
        self.headers_map = upcase_keys(headers_map or {})
        if self.headers_map.get('Content-Type') is None:
            self.headers_map['Content-Type'] = default_media_type


    @property
    def status(self):
        return self._status


    @property
    def status_line(self):
        return 'HTTP/1.1 ' + str(self.status) + ' ' + STATUS_MAP.get(self.status, 'UNKNOWN')

    
    @property
    def body(self):
        if self._body is None and self.status > 399:
           self._body = {'message': STATUS_MAP.get(self.status, 'Unknown Error')}

        if self.headers_map['Content-Type'].startswith('application/json') and isinstance(self._body, collections.abc.Mapping):
            return json.dumps(self._body)

        return self._body


    @property
    def headers_lines(self):
        h = self.headers_map
        headers = list(map(lambda k: k + ': ' + h[k], h.keys()))
        headers.append('Server: andyweb/1.0 (A Python Thing)')
        headers.append('Date: ' + datetime.isoformat(datetime.now()))
        if self.headers_map.get('Content-Type') is None:
            headers.append('Content-Type: application/json; charset=utf-8')
        if self.body is not None:
            headers.append('Content-Length: ' + str(len(self.body)))
        if self.headers_map.get('Connection') is None:
            headers.append('Connection: keep-alive')

        return RN.join(headers)


    @property
    def bytes(self):
        response_string = RN.join([self.status_line, self.headers_lines]) + RN + RN
        response_string += self.body or ''
        return bytes(response_string, 'utf-8')
    
