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


    def get_handler(self, request):
        print('looking for ', request.resource)
        return self._routes.get(request.resource, not_found)
