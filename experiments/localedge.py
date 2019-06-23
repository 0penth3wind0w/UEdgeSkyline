import os, sys
sys.path.append(os.path.abspath(os.pardir))

import pickle

from data.dataClass import Data, batchImport
from skyline.slideUPSky import slideUPSky
from visualize import visualize

if __name__ == "__main__":
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
            pickle.dump(result, f)
    
    usky.removeRtree()
