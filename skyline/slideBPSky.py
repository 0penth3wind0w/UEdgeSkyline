# Sliding window brute force PSky
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time
from rtree import index

from data.dataClass import Data, batchImport
from visualize.visualize import visualize
from dominate import dominateStat

class slideBPSky():
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
        pruned = self.window.copy()
        clean = self.window.copy()
        # pruning
        for d in self.window.copy():
            # cascade purning method. Inspired from "Efficient Computation of Group Skyline Queries on MapReduce (FCU)"
            if d in clean:
                pastart = [self.drange[1] if i+2*self.radius+0.1>self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                pamax = [self.drange[1] for j in range(self.dim)]
                # prune data points that are obviously dominated by current data point
                parea = (self.index.intersection(tuple(pastart+pamax),objects=True))
                for p in parea:
                    if p.object in clean:
                        clean.remove(p.object)
        for d in clean:
            pruned.remove(d)
        for d in pruned.copy():
            if d in pruned:
                pastart = [self.drange[1] if i+2*self.radius+0.1>self.drange[1] else i+2*self.radius+0.1 for i in d.getLocationMax()]
                pamax = [self.drange[1] for j in range(self.dim)]
                # prune data points that are obviously dominated by current data point
                parea = (self.index.intersection(tuple(pastart+pamax),objects=True))
                for p in parea:
                    if p.object in pruned:
                        pruned.remove(p.object)
        self.skyline = clean
        self.skyline2 = pruned
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
    test = slideBPSky(2, 5, 4, [0,1000], wsize=100)
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