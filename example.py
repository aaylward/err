import logging

from pystuff.resource import Resource
from pystuff.response import Response
from pystuff.router import Router
from pystuff.server import Server

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    router = Router().\
            with_route(Resource('', 'GET'), lambda req: Response(200, 'sup', {'Content-Type': 'text/plain'})).\
            with_route(Resource('/hi', 'GET'), lambda req: Response(200, 'hi', {'Content-Type': 'text/plain'}))
    server = Server(router=router)
    server.run()

if __name__ == '__main__':
    main()

