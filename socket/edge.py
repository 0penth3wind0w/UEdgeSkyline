import os, sys
sys.path.append(os.path.abspath(os.pardir))

import configparser
import socket
import pickle

from data.dataClass import Data, batchImport
from skyline.slideUPSky import slideUPSky

class Edge():
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def send(self, sky1, sky2):
        # Process data
        data = {'SK1':sky1, 'SK2':sky2}
        sdata = pickle.dumps(data)
        # Create a socket (SOCK_STREAM means a TCP socket) and send data
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:        
            # Connect to server and send data
            sock.connect((self.host, self.port))
            sock.sendall(sdata)
        # received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(data))
        # print("Received: {}".format(received))

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('edge.config')
    PORT = int(config['DEFAULT'].get('Port'))
    HOST = config['DEFAULT'].get('Host')

    edge = Edge(HOST,PORT)
    usky = slideUPSky(2, 5, 4, [0,1000], wsize=100)
    dqueue = batchImport('1500_dim2_pos5_rad5_01000.csv', 5)
    
    for i in range(10):
        usky.receiveData(dqueue[i])
        usky.updateSkyline()
        edge.send(usky.getSkyline(),usky.getSkyline2())
        
    usky.removeRtree()
    