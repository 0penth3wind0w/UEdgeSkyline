import os, sys
sys.path.append(os.path.abspath(os.pardir))

import configparser
import socket
import pickle

from data.dataClass import Data, batchImport
from skyline.slideUPSky import slideUPSky

from visualize import visualize

class Edge():
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def send(self, updateInfo):
        sdata = pickle.dumps(updateInfo)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:        
            # Connect to server and send data
            sock.connect((self.host, self.port))
            sock.sendall(sdata)
        # received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(updateInfo))
        # print("Received: {}".format(received))

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('edge.config')
    PORT = int(config['DEFAULT'].get('Port'))
    HOST = config['DEFAULT'].get('Host')

    edge = Edge(HOST,PORT)
    usky = slideUPSky(2, 5, 4, [0,1000], wsize=10)
    dqueue = batchImport('1500_dim2_pos4_rad5_01000.csv', 4)
    
    with open('pickle_edge.pickle', 'wb') as f:
        for i in range(15):
            oldsk = usky.getSkyline().copy()
            oldsk2 = usky.getSkyline2().copy()
            usky.receiveData(dqueue[i])
            out = usky.getOutdated().copy()
            usky.updateSkyline()
            usk1 = list(set(usky.getSkyline())-set(oldsk))
            usk2 = list(set(usky.getSkyline2())-set(oldsk2))
            result = {'Delete':out,'SK1':usk1,'SK2':usk2}
            # edge.send(result)
            pickle.dump(result, f)
            # print('SK1')
            # for d in usky.getSkyline():
            #     print(d.getLabel())
            # print('SK2')
            # for d in usky.getSkyline2():
            #     print(d.getLabel())
            # print()
            # input()
    visualize.visualize(usky.getSkyline(),4,[0,1000])
    visualize.visualize(usky.getSkyline2(),4,[0,1000])
    usky.removeRtree()
