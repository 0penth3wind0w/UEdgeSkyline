import os, sys
sys.path.append(os.path.abspath(os.pardir))

import pickle

from data.dataClass import Data, batchImport

if __name__ == "__main__":
    edge0data = []
    with open('pickle_edge0.pickle', 'rb') as f:
        for i in range(5000):
            edge0data.append(pickle.load(f))
    
    edge1data = []
    with open('pickle_edge1.pickle', 'rb') as f:
        for i in range(5000):
            edge1data.append(pickle.load(f))
    
    with open('pickle_edge.pickle', 'wb') as f:
        for i in range(5000):
            pickle.dump(edge0data.pop(0), f)
            pickle.dump(edge1data.pop(0), f)