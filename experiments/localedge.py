import os, sys
sys.path.append(os.path.abspath(os.pardir))

import pickle
import time

from data.dataClass import Data, batchImport
from skyline.slideUPSky import slideUPSky
from visualize import visualize

if __name__ == "__main__":
    eid = input("Edge id: ")
    usky = slideUPSky(2, 5, 5, [0,1000], wsize=300)
    dqueue = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    
    idx = [i for i in range(10000) if i%2 == 1]
    with open('pickle_edge'+eid+'.pickle', 'wb') as f:
        start_time = time.time()
        for i in idx:
            oldsk = usky.getSkyline().copy()
            oldsk2 = usky.getSkyline2().copy()
            usky.receiveData(dqueue[i])
            out = usky.getOutdated().copy()
            usky.updateSkyline()
            usk1 = list(set(usky.getSkyline())-set(oldsk))
            usk2 = list(set(usky.getSkyline2())-set(oldsk2))
            result = {'Delete':out,'SK1':usk1,'SK2':usk2}
            pickle.dump(result, f)
        print("--- %s seconds ---" % (time.time() - start_time))
    
    usky.removeRtree()
