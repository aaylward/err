from datetime import datetime
from .response import Response


def not_found(request):
    return Response(404)


class Router(object):
    def __init__(self, routes=None):
        self._routes = routes or {}


    def get_handler(self, request):
        return self._routes.get(request.resource(), not_found)
