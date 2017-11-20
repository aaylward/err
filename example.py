import logging
import os

from pytip.resource import Resource
from pytip.response import Response
from pytip.router import Router
from pytip.server import Server

logging.basicConfig(format='%(levelname)s:%(message)s\n', level=logging.DEBUG)

CWD = os.getcwd()

MOVIES = {'guitar': os.path.join(CWD, 'guitar.mov')}

def handle_post(request):
    return Response(200, {'message': 'ack', 'req': request.body})


def say_hi(request):
    return Response(200, {'message': 'hi ' + request.qs.get('name', ['friend'])[0]})


def handle_vid(request):
    vid_name = request.qs.get('name', [''])[0]

    if MOVIES.get(vid_name) is not None:
        return Response(200, file_name=MOVIES.get(vid_name))
    else:
        return Response(404)


def main(*args):
    router = Router() \
            .with_route(Resource('', 'GET'), lambda req: Response(200, 'sup', {'Content-Type': 'text/plain'})) \
            .with_route(Resource('/p', 'POST'), handle_post) \
            .with_route(Resource('/vid', 'GET'), handle_vid) \
            .with_route(Resource('/err', 'GET'), lambda req: 1/0) \
            .with_route(Resource('/hi', 'GET'), say_hi)
    server = Server(router=router)
    server.run()

if __name__ == '__main__':
    main()

