import logging

from pystuff.resource import Resource
from pystuff.response import Response
from pystuff.router import Router
from pystuff.server import Server

logging.basicConfig(format='%(levelname)s:%(message)s\n', level=logging.DEBUG)

def handle_post(request):
    return Response(200, {'message': 'ack', 'req': request.body})

def say_hi(request):
    return Response(200, {'message': 'hi ' + request.qs.get('name', ['friend'])[0]})

def main():
    router = Router() \
            .with_route(Resource('', 'GET'), lambda req: Response(200, 'sup', {'Content-Type': 'text/plain'})) \
            .with_route(Resource('/p', 'POST'), handle_post) \
            .with_route(Resource('/err', 'GET'), lambda req: 1/0) \
            .with_route(Resource('/hi', 'GET'), say_hi)
    server = Server(router=router)
    server.run()

if __name__ == '__main__':
    main()

