import os, sys
sys.path.append(os.path.abspath(os.pardir))

import random
from matplotlib import pyplot as plt
from data.dataClass import Data, batchImport

if __name__ == '__main__':
    datalist = batchImport('data_rec50_dim2_pos3_rad3.csv', 3)
    answer = input('Would you like to change the csv file? (Y/N)')
    if answer == 'Y':
        csv = input('Please specify the csv file name in data folder: ')
        pcount = input('Please input the probability count: ')
        datalist = batchImport('data_rec50_dim2_pos3_rad3.csv', 3)

    plt.figure()
    for d in datalist:
        #rgb = [random.randint(0,255) for i in range(3)]
        x = [d.getLocation(0)[0],d.getLocation(1)[0],d.getLocation(2)[0]]
        y = [d.getLocation(0)[1],d.getLocation(1)[1],d.getLocation(2)[1]]
        plt.scatter(x,y,alpha=0.5)
    plt.show()