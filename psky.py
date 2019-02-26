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
    def getLocation(self, index):
        try:
            return [self.prob[index], self.plocation[index]]
        except:
            return []

def batchImport(csvfile):
    result = []
    with open(here+'/data/'+csvfile, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for row in csv_reader:
            print(row)


if __name__ == '__main__':
    # test = Data('d_1', 3)
    # test.insertLocation(0.3, [2,6])
    # test.insertLocation(0.2, [6,4])
    # test.insertLocation(0.5, [8,7])
    # print(test.getLocation(0))
    # print(test.getLocation(1))
    # print(test.getLocation(2))
    # print(test.getLocation(3))
    batchImport('data_50r2d3p.csv')
