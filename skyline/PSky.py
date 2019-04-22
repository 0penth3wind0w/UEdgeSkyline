# Sliding window PSky super class 
import os, sys
sys.path.append(os.path.abspath(os.pardir))

from rtree import index

class PSky():
    def __init__(self, dim, ps, radius, drange, wsize):
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
    def getOutdated(self):
        """
        Get current outdated data
        """
        return self.outdated
    def removeRtree(self):
        """
        Remove rtree data and index file
        """
        try:
            os.remove(str(self.dim)+'d_index.data')
            os.remove(str(self.dim)+'d_index.index')
            print('Files removed')
        except:
            print('No such files')

if __name__ == '__main__':
    pass