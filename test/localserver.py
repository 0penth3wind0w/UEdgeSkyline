import os, sys
sys.path.append(os.path.abspath(os.pardir))

import pickle

from data.dataClass import Data
from skyline.PSky import PSky
from visualize import visualize

# PSky class use only in server side 
class servePSky(PSky):
    def __init__(self, dim, ps, radius, drange=[0,1000], wsize=10):
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
            Note that the window size should be sum(edge window)
        """
        PSky.__init__(self, dim, ps, radius, drange, wsize)
    def receive(self,data):
        """
        Update data received by server

        :param data: dict
            json format(dict) data include change of an edge node.
            Delete: outdated data
            SK1: new data in skyline set
            SK2: new data in skyline2 set
        """
        if len(data['Delete']) > 0:
            for d in data['Delete']:
                self.window.remove(d)
                self.outdated.append(d)
                self.updateIndex(d, 'remove')
        if len(data['SK1']) > 0:
            for d in data['SK1']:
                if d not in self.window:
                    self.window.append(d)
                    self.skyline.append(d)
                    self.updateIndex(d, 'insert')
                elif d in self.skyline2:
                    self.skyline2.remove(d)
                    self.skyline.append(d)
                # ignore other condition
        if len(data['SK2']) > 0:
            for d in data['SK2']:
                if d not in self.window:
                    self.window.append(d)
                    self.skyline2.append(d)
                    self.updateIndex(d, 'insert')
                elif d in self.skyline:
                    self.skyline.remove(d)
                    self.skyline2.append(d)
                # ignore other condition
        self.update()
    def update(self):
        """
        Update global skyline set
        """
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
            # Clear outdated data
            self.outdated = []
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

if __name__ == "__main__":
    skyServer = servePSky(2, 5, 4, drange=[0,1000], wsize=10)

    with open('pickle_edge.pickle', 'rb') as f:
        for i in range(15):
            data = pickle.load(f)
            skyServer.receive(data)
            skyServer.update()
    
    skyServer.removeRtree()