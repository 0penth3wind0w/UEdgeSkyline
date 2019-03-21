import os, sys
sys.path.append(os.path.abspath(os.pardir))

import configparser
import socket
import pickle

from data.dataClass import Data, batchImport

config = configparser.ConfigParser()
config.read('edge.config')
PORT = int(config['DEFAULT'].get('Port'))
HOST = config['DEFAULT'].get('Host')

# Create a socket (SOCK_STREAM means a TCP socket) and send data
def edgeSend(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((host, port))
        sock.sendall(data)
        # received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(data))
        # print("Received: {}".format(received))

if __name__ == "__main__":
    # data = " TESTDATA "
    dlist = batchImport('test_rec30_dim3_pos3_rad2.csv', 3)
    for d in dlist:
        data = pickle.dumps(d)
        edgeSend(HOST,PORT,data)
    