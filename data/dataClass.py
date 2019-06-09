import os
import csv
import numpy as np
import random

here = os.path.dirname(os.path.abspath(__file__))

class Data():
    """Class use to store data information"""
    def __init__(self, name, ps):
        """
        Initializer

        :param name: string
            The name (or label) of the data
        :param ps: int
            Instance count of the data. 
        """
        self.name = name
        self.pprob = ps
        self.probs = []
        self.locations = []
        self.regionMax = []
        self.regionMin = []
    def __updateMinMax(self, loc):
        """
        For use inside the class only.
        Use to update the bounding region.

        :param loc: list(int)
            the new location instance which added to data object
        """
        if self.regionMax == []:
            self.regionMax = loc.copy()
        else:
            for i, lu in enumerate(loc):
                if self.regionMax[i] < lu:
                    self.regionMax[i] = lu
        if self.regionMin == []:
            self.regionMin = loc.copy()
        else:
            for j, lm in enumerate(loc):
                if self.regionMin[j] > lm:
                    self.regionMin[j] = lm
    def insertLocation(self, prob, location):
        """
        Insert a new instance of data object.

        :param prob: float
            the probability of the new coming instance.
        :param location: list(int)
            the location of the new coming instance.
        """
        self.probs.append(prob)
        self.locations.append(location)
        self.__updateMinMax(self.locations[-1])
    def getLabel(self):
        """
        Get the name(label) of the data object
        """
        return self.name
    def getPCount(self):
        """
        Get the total instance count of the data object
        """
        return self.pprob
    def getProbLocSet(self, index):
        """
        Get a list which contain the occurance probability and instance location according to given index.
        If the given index exceed, the function will return [None, []]

        :param index: int
            The index of location, according to insertion sequence.(0 to n-1)         
        """
        try:
            return [self.probs[index], self.locations[index]]
        except:
            return [None, []]
    def getProb(self, index):
        """
        Get the occurance probability of instance according to given index.
        If the given index exceed, the function will return None
        
        :param index: int
            The index of occurance probability, according to insertion sequence.(0 to n-1)         
        """
        try:
            return self.probs[index]
        except:
            return None
    def getLocation(self, index):
        """
        Get the instance location according to given index.
        If the given index exceed, the function will return an empty list.
        
        :param index: int
            The index of instance location, according to insertion sequence.(0 to n-1)         
        """
        try:
            return self.locations[index]
        except:
            return []
    def getLocationMax(self):
        """
        Get the list which contains the maximium value of data location for each dimension.    
        """
        return self.regionMax
    def getLocationMin(self):
        """
        Get the list which contains the minimium value of data location for each dimension.    
        """
        return self.regionMin
    def getMinMaxTuple(self):
        """
        Get the suple which contains the minimium and maximium value of data location for each dimension.
        This function is use with rtree.
        The format of the tuple is: (d1min, d2min,..., dnmin, d1max, d2max,..., dnmax)     
        """
        return tuple(self.regionMin+self.regionMax)
    
    # Override default function
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    def __str__(self):
        return str(self.__dict__)
    def __hash__(self):
        return hash(str(self.__dict__))

def batchImport(csvfile, ps):
    """
    Import data objects using csv file.
    This function returns a list of data object.
    
    :param csvfile: srting
        the .csv file locate in data/ of this project
    :param ps: float
        instance count of an object
    """
    result = []
    with open(here+'/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            data = Data(row[0], ps)
            for p in range(ps):
                # Some awful string manipulation to parse numbers
                data.insertLocation(float(row[2*p+1]), [int(float(i)) for i in row[2*p+2].strip(' []').split(',')])
            result.append(data)
    return result


if __name__ == '__main__':
    data = batchImport('test_rec30_dim3_pos3_rad2.csv',3)
