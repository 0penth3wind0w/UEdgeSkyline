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
    def sendSK(self, sky1, sky2):
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
    def sendOdt(self,outdated):
        # Process data
        data = {'Delete':outdated}
        sdata = pickle.dumps(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:        
            # Connect to server and send data
            sock.connect((self.host, self.port))
            sock.sendall(sdata)
        # received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(data))
        # print("Received: {}".format(received))
    def sendUdt(self, belong,update):
        # Process data
        data = {belong:update}
        sdata = pickle.dumps(data)
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
    usky = slideUPSky(2, 5, 4, [0,1000], wsize=10)
    dqueue = batchImport('1500_dim2_pos4_rad5_01000.csv', 4)
    
    for i in range(100):
        oldsk = usky.getSkyline().copy()
        oldsk2 = usky.getSkyline2().copy()
        usky.receiveData(dqueue[i])
        if len(usky.getOutdated()) != 0:
            edge.sendOdt(usky.getOutdated())
        usky.updateSkyline()
        usk1 = list(set(usky.getSkyline())-set(oldsk))
        if len(usk1) != 0:
            edge.sendUdt('SK1',usk1)
        usk2 = list(set(usky.getSkyline2())-set(oldsk2))
        if len(usk2) != 0:
            edge.sendUdt('SK2',usk2)
        # edge.sendSK(usky.getSkyline(),usky.getSkyline2())
    usky.removeRtree()
    