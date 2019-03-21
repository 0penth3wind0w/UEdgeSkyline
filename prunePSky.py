import os, sys
sys.path.append(os.path.abspath(os.pardir))

from rtree import index

from data.dataClass import Data, batchImport
from visualize.visualize import visualize

from dominate import dominateStat

class brutePSky():
    def __init__(self, ps, radius=3):
        """
        Initializer

        :param ps: int
            The occurance count of the instance.
        :param radius: int
            radius use to prevent data being pruned unexpectedly.
            Recommand to be set according to the name of .csv file.
        """
        self.ps = ps
        self.radius = radius
        self.data = []
        self.pruned = []
        self.index = None
        self.dim = 0
    def loadData(self, file):
        """
        Load data from csv file
        """
        self.data = batchImport(file, self.ps)
    def createIndex(self, dim):
        """
        Create rtree index

        :param dim: int
            dimension of data
        """
        p = index.Property()
        p.dimension = dim
        self.dim = dim
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        idx = index.Index(str(dim)+'d_index',properties=p)
        for d in self.data:
            idx.insert(1, d.getMinMaxTuple(),obj=d)
        self.index = idx
    def pruning(self):
        """
        Prune the unnecessary Data objects
        """
        data = self.data.copy()
        for d in self.data:
            if d in data:
                pastart = [100 if i+self.radius>100 else i+self.radius for i in d.getLocationMax()]
                pamax = [100 for j in range(self.dim)]    
                pruned = (self.index.intersection(tuple(pastart+pamax),objects=True))
                for p in pruned:
                    if p.object in data:
                        data.remove(p.object)
        self.pruned = data
    def calculateUSky(self):
        skyline = []
        for p in self.pruned:
            pastart = [0 for i in range(self.dim)]
            pamax = p.getLocationMax()
            pdom = list(self.index.intersection(tuple(pastart+pamax),objects=True))
            if len(pdom) == 1 and pdom[0].object == p:
                skyline.append([p, 1.0])
            else:
                finalp = 0.0
                for i in range(p.getPCount()):
                    base = p.getProb(i)
                    loc = p.getLocation(i)
                    intersec = list(self.index.intersection(tuple(pastart+loc),objects=True))
                    for d in intersec:
                        dobj = d.object
                        if dobj != p:
                            tprob = 0.0
                            for idx in range(dobj.getPCount()):
                                if dominateStat(dobj.getLocation(idx),loc) == True:
                                    tprob += dobj.getProb(idx)
                            tprob = 1.0 - tprob
                            base *= tprob
                    finalp += base
                skyline.append([p, finalp])

        print(skyline)
    def getOrigin(self):
        """
        Get the list of Data objects before pruning.
        """
        return self.data
    def getPruned(self):
        """
        Get the list of Data objects after pruning.
        """
        return self.pruned
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
    test = brutePSky(5, radius=4)
    test.loadData('data_rec50_dim2_pos5_rad4.csv')
    test.createIndex(2)
    test.pruning()
    test.calculateUSky()
    visualize(test.getOrigin(),5)
    visualize(test.getPruned(),5)
    test.removeRtree()