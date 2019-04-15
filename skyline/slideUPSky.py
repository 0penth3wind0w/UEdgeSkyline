# Sliding window update PSky
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time
from rtree import index

from data.dataClass import Data, batchImport
from visualize.visualize import visualize
from dominate import dominateStat

class slideUPSky():
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
        self.dim = dim # data dimension
        self.ps = ps # possible instance count
        self.radius = radius # radius of a data
        self.drange = drange # data range
        self.wsize = wsize # sliding window size
        self.window = [] # sliding window
        self.skyline = [] # 1st set skyline candidate
        self.skyline2 = [] # 2nd set skyline candidate
        self.outdated = [] # temporary storage for outdated data
        p = index.Property()
        p.dimension = dim
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        self.index = index.Index(str(dim)+'d_index',properties=p) # r-tree index
    def receiveData(self, d):
        """
        Receive one new data.

        :param d: Data
            The received data
        """
        if len(self.window) >= self.wsize:
            self.updateIndex(self.window[0], "remove")
            self.outdated.append(self.window[0])
            del self.window[0]
        self.window.append(d)
        self.updateIndex(d,"insert")
    def updateIndex(self, d, op):
        """
        Update R-Tree index

        :param d: Data
            The data to be insert/delete
        :param op: str
            'insert' indicate data insertion
            'remove' indicate the removal of data
        """
        if op == 'insert':
            id = int(d.getLabel()[2:])
            self.index.insert(id, d.getMinMaxTuple(),obj=d)
        elif op == 'remove':
            id = int(d.getLabel()[2:])
            self.index.delete(id,d.getMinMaxTuple())
        else:
            print("error")
    def updateSkyline(self):
        # skyline = self.skyline.copy()
        # skyline2 = self.skyline2.copy()
        if len(self.outdated) > 0:
            # Remove outdated data in sk2
            for d in self.outdated:
                if d in self.skyline2:
                    self.skyline2.remove(d)
            # Remove outdated data in sk, add sk2 data to sk when needed
            for d in self.outdated:
                if d in self.skyline:
                    self.skyline.remove(d)
                    sstart = [ i for i in d.getLocationMax()]
                    send = [self.drange[1] for i in range(self.dim)]
                    search = [ p.object for p in (self.index.intersection(tuple(sstart+send),objects=True))]
                    for sd in search:
                        if sd in self.skyline2:
                            self.skyline2.remove(sd)
                            self.skyline.append(sd)
            # clear outdated temp
            del self.outdated[0]
        # filter out new points
        newdata = self.window[-1]
        # append new point into sk
        self.skyline.append(newdata)
        # prune objects in sk, move data dominated by other sk point to sk2
        for d in self.skyline.copy():
            if d in self.skyline:
                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                vurend = [ self.drange[1] for i in range(self.dim)]
                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
                for p in vur:
                    if p in self.skyline:
                        self.skyline.remove(p)
                        self.skyline2.append(p)
        # prune objects in sk2
        for d in self.skyline2.copy():
            if d in self.skyline2:
                vurstart = [ self.drange[1] if i+2*self.radius+0.1 > self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                vurend = [ self.drange[1] for i in range(self.dim)]
                vur = [ p.object for p in (self.index.intersection(tuple(vurstart+vurend),objects=True))]
                for p in vur:
                    if p in self.skyline2:
                       self.skyline2.remove(p)
        # self.skyline = skyline
        # self.skyline2 = skyline2
    def getWindow(self):
        return self.window
    def getSkyline(self):
        """
        Get the 1st set of skyline candidate.
        """
        return self.skyline
    def getSkyline2(self):
        """
        Get the 2nd set of skyline candidate.
        """
        return self.skyline2
    def removeRtree(self):
        """
        remove rtree data and index file
        """
        try:
            os.remove(str(self.dim)+'d_index.data')
            os.remove(str(self.dim)+'d_index.index')
            print('Files removed')
        except:
            print('No such files')

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