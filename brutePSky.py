import os, sys
sys.path.append(os.path.abspath(os.pardir))

from rtree import index
from data.dataClass import Data, batchImport
from visualize.visualize import visualize

here = os.path.dirname(os.path.abspath(__file__))

class brutePSky():
    def __init__(self, ps, radius=3):
        self.ps = ps
        self.radius = radius
        self.data = []
        self.result = []
        self.index = None
        self.dim = 0
    def loadData(self, file):
        self.data = batchImport(file, self.ps)
    def createIndex(self, dim):
        p = index.Property()
        p.dimension = dim
        self.dim = dim
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        idx = index.Index(str(dim)+'d_index',properties=p)
        for d in self.data:
            idx.insert(1, d.getMinMaxTuple(),obj=d)
        self.index = idx
    def readIndex(self):
        return self.index
    def calculatePSky(self):
        data = self.data.copy()
        for d in data:
            pastart = [100 if i+self.radius>100 else i+self.radius for i in d.getLocationMax()]
            pamax = [100 for j in range(self.dim)]
            pruned = (self.index.intersection(tuple(pastart+pamax),objects=True))
            for p in pruned:
                for d in data:
                    if p.object.isEqual(d):
                        data.remove(d)
        self.result = data
    def getOrigin(self):
        return self.data
    def getResult(self):
        return self.result
    def removeRtree(self):
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
    test.calculatePSky()
    visualize(test.getOrigin(),3)
    visualize(test.getResult(),3)
    test.removeRtree()