import os, sys
sys.path.append(os.path.abspath(os.pardir))

import pickle

from data.dataClass import Data, batchImport

with open('pickle_edge.pickle', 'rb') as f:
    for i in range(15):
        a = pickle.load(f)
        print(a)