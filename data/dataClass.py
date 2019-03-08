import os
import csv
import numpy as np
import random

here = os.path.dirname(os.path.abspath(__file__))

# Class use to store data information
class Data():
    def __init__(self, name, ps):
        self.name = name
        self.pprob = ps
        self.probs = []
        self.locations = []
        self.regionMax = []
        self.regionMin = []
    def __updateMinMax__(self, location):
        for i, axis in enumerate(location):
            if axis > self.regionMax[i]:
                self.regionMax[i] = axis
            if axis < self.regionMin[i]:
                self.regionMin[i] = axis
    def insertLocation(self, prob, location):
        self.probs.append(prob)
        self.locations.append(location)
        if self.regionMax == [] and self.regionMin == []:
            self.regionMax = location
            self.regionMin = location
        else:
            self.__updateMinMax__(location)
    def getLabel(self):
        return self.name
    def getPCount(self):
        return self.pprob
    def getProbLocSet(self, index):
        try:
            return [self.probs[index], self.locations[index]]
        except:
            return [None, []]
    def getProb(self, index):
        try:
            return self.probs[index]
        except:
            return None
    def getLocation(self, index):
        try:
            return self.locations[index]
        except:
            return []
    def getLocationMax(self):
        return self.regionMax
    def getLocationMin(self):
        return self.regionMin

# batchImpor import data from csv file and return the list of data
# ps is the possoble count of data
def batchImport(csvfile, ps):
    result = []
    with open(here+'/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            data = Data(row[0], ps)
            for p in range(ps):
                # Some awful string manipulation to parse numbers
                data.insertLocation(float(row[2*p+1]), [int(i) for i in row[2*p+2].strip(' []').split(',')])
            result.append(data)
    return result


if __name__ == '__main__':
    data = batchImport('data_rec50_dim2_pos3_rad3.csv',3)

