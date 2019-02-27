import os

from dataClass import Data, batchImport

here = os.path.dirname(os.path.abspath(__file__))

class brutePSky():
    def __init__(self, ps):
        self.ps = ps
        self.data = []
        self.result = []
    def loadData(self, file):
        self.data = batchImport(file, self.ps)
    def calculatePSky(self):
        return None
    def getResult(self):
        return self.result

if __name__ == '__main__':
    None