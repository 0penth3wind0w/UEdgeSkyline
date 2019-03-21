import os, sys
sys.path.append(os.path.abspath(os.pardir))

import configparser
import socketserver
import pickle

from data.dataClass import Data

config = configparser.ConfigParser()
config.read('edge.config')
PORT = int(config['DEFAULT'].get('Port'))
HOST = config['DEFAULT'].get('Host')

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4096)
        receive = pickle.loads(self.data)
        
        print(receive)
        print(type(receive))
        
        # self.request.sendall(self.data.upper())

if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()