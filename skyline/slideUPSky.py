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
        # filter out new points
        newdata = self.window[-1]
        # append new point into sk
        skyline.append(newdata)
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
    test = slideUPSky(2, 5, 4, [0,1000], wsize=100)
    dqueue = batchImport('test_1500_dim2_pos5_rad5_01000.csv', 5)
    start_time = time.time()
    for i in range(1500):
        test.receiveData(dqueue[i])
        test.updateSkyline()
        # if i%100 == 0:
        #     print("Window: "+str(len(test.getWindow())))
        #     print("Sk: "+ str(len(test.getSkyline())))
        #     # for each in test.getSkyline():
        #     #     print(each)
        #     print("Sk2: "+ str(len(test.getSkyline2())))
        #     visualize(test.getWindow(), 5, [0,1000])
        #     visualize(test.getSkyline(), 5, [0,1000])
        #     visualize(test.getSkyline2(), 5, [0,1000])
        #     print()
    test.removeRtree()
    print("--- %s seconds ---" % (time.time() - start_time))