import os
import csv
import numpy as np
import random

here = os.path.dirname(os.path.abspath(__file__))

# Class use to store data information
class Data():
    def __init__(self, name, probs):
        self.name = name
        self.probs = probs
        self.prob = []
        self.plocation = []
    def insertLocation(self, prob, location):
        self.prob.append(prob)
        self.plocation.append(location)
    def getLabel(self):
        return self.name
    def getLocation(self, index):
        try:
            return [self.prob[index], self.plocation[index]]
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

