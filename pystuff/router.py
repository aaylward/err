from datetime import datetime

from .response import Response


def not_found(request):
    return Response(404)


class Router(object):
    def __init__(self, routes=None):
        self._routes = routes or {}


    def with_route(self, resource, handler):
        self._routes[resource] = handler
        return self


    def _get_handler(self, request):
        return self._routes.get(request.resource, not_found)


    def route(self, request):
        handler = self._get_handler(request)
        return handler.__call__(request)

