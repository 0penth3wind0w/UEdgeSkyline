# Sliding window update PSky
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time
from rtree import index

from skyline.PSky import PSky
from data.dataClass import Data, batchImport
from visualize.visualize import visualize

class slideUPSky(PSky):
    def __init__(self, dim, ps, radius, drange=[0,100], wsize=10):
        """
        Initializer

        :param dim: int
            The dimension of data
        :param ps: int
            The occurance count of the instance.
        :param radius: int
            radius use to prevent data being pruned unexpectedly.
            Recommand to be set according to the name of .csv file.
        :param drange: list(int)
            data range [min, max]
        :param wsize: int
            Size of sliding window.
        """
        PSky.__init__(self, dim, ps, radius, drange, wsize)
        self.newdata = []
    def receiveData(self, d):
        """
        Receive one new data.

        :param d: Data
            The received data
        """
        if len(self.window) >= self.wsize:
            self.updateIndex(self.window[0], 'remove')
            self.outdated.append(self.window[0])
            del self.window[0]
        self.window.append(d)
        self.newdata.append(d)
        self.updateIndex(d,'insert')
    def updateSkyline(self):
        skyline = self.skyline.copy()
        skyline2 = self.skyline2.copy()
        if self.outdated: # check empty or nor (False if empty)
            # Remove outdated data in sk2
            for d in self.outdated.copy():
                if d in skyline2:
                    skyline2.remove(d)
                    self.outdated.remove(d)
        if self.outdated:
            # Remove outdated data in sk, add sk2 data to sk when needed
            for d in self.outdated:
                if d in skyline:
                    skyline.remove(d)
                    sstart = [ i for i in d.getLocationMax()]
                    send = [self.drange[1] for i in range(self.dim)]
                    search = (self.index.intersection(tuple(sstart+send),objects=True))
                    for sd in search:
                        if sd.object in skyline2:
                            skyline2.remove(sd.object)
                            skyline.append(sd.object)
        # clear outdated temp
        self.outdated.clear()
        # append new point into sk
        for d in self.newdata:
            skyline.append(d)
        # clear newdata temp
        self.newdata.clear()
        # prune objects in sk, move data dominated by other sk point to sk2
        for d in skyline.copy():
            if d in skyline:
                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                vurend = [ self.drange[1] for i in range(self.dim)]
                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
                for p in vur:
                    if p in skyline:
                        skyline.remove(p)
                        skyline2.append(p)
        # prune objects in sk2
        for d in skyline2.copy():
            if d in skyline2:
                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                vurend = [ self.drange[1] for i in range(self.dim)]
                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
                for p in vur:
                    if p in skyline2:
                       skyline2.remove(p)
        self.skyline = skyline
        self.skyline2 = skyline2

if __name__ == '__main__':
    test = slideUPSky(5, 5, 5, [0,1000], wsize=24)
    dqueue = batchImport('data.csv', 5)
    
    # prevsk1 = []
    # prevsk2 = []
    
    # with open('result.txt', 'a') as f:
    #     f.write("o_Delete,o_SK1,o_SK2,a_Delete,a_SK1,a_SK2\n")
    start_time = time.time()
    for i in range(827):
        test.receiveData(dqueue[i])
        # out = test.getOutdated().copy()
        test.updateSkyline()
        # usk1 = list(set(test.getSkyline())-set(prevsk1))
        # usk2 = list(set(test.getSkyline2())-set(prevsk2))
        # orig = {'Delete':out,'SK1':test.getSkyline(),'SK2':test.getSkyline2()}
        # arch = {'Delete':out,'SK1':usk1,'SK2':usk2}
        
        # with open('result.txt', 'a') as f:
        #     f.write(str(len(orig['Delete']))+','+str(len(orig['SK1']))+','+str(len(orig['SK2']))+','+str(len(arch['Delete']))+','+str(len(arch['SK1']))+','+str(len(arch['SK2']))+'\n')
        
        # prevsk1 = test.getSkyline().copy()
        # prevsk2 = test.getSkyline2().copy()

    test.removeRtree()
    print("--- %s seconds ---" % (time.time() - start_time))