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
    def insertLocation(self, prob, location):
        self.probs.append(prob)
        self.locations.append(location)
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
    

# batchImpor import data from csv file and return the list of data
# ps is the possoble count of data
def batchImport(csvfile, ps):
    result = []
    with open(here+'/data/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            data = Data(row[0], ps)
            for p in range(ps):
                # Some awful string manipulation to parse numbers
                data.insertLocation(float(row[2*p+1]), [int(i) for i in row[2*p+2].strip(' []').split(',')])
            result.append(data)
    return result


if __name__ == '__main__':
    
    data = batchImport('data_50r2d3p.csv',3)

