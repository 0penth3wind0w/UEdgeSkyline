import os, sys
sys.path.append(os.path.abspath(os.pardir))

from rtree import index
from data.dataClass import Data, batchImport
from visualize.visualize import visualize

here = os.path.dirname(os.path.abspath(__file__))

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
        Prune the unnecessary Dara objects
        """
        data = self.data.copy()
        for d in data:
            pastart = [100 if i+self.radius>100 else i+self.radius for i in d.getLocationMax()]
            pamax = [100 for j in range(self.dim)]
            pruned = (self.index.intersection(tuple(pastart+pamax),objects=True))
            for p in pruned:
                for d in data:
                    if p.object.isEqual(d):
                        data.remove(d)
        self.pruned = data
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
            os.remove(str(self.ps)+'d_index.data')
            os.remove(str(self.ps)+'d_index.index')
            print('Files removed')
        except:
            print('No such files')

if __name__ == '__main__':
    test = brutePSky(3)
    test.loadData('test_rec30_dim3_pos3_rad2.csv')
    test.createIndex(3)
    test.pruning()
    visualize(test.getOrigin(),3)
    visualize(test.getPruned(),3)
    test.removeRtree()