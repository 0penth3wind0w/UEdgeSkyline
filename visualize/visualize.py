import os, sys
sys.path.append(os.path.abspath(os.pardir))

import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from data.dataClass import Data, batchImport

def visualize(datalist, pcount):
    dim = len(datalist[0].getLocation(0))
    print(dim)
    fig = plt.figure()
    if dim == 2:
        for d in datalist:
            x = [d.getLocation(i)[0] for i in range(pcount)]
            y = [d.getLocation(j)[1] for j in range(pcount)]
            plt.scatter(x,y,alpha=0.5)        
    elif dim == 3:
        ax = fig.add_subplot(111, projection='3d')
        for d in datalist:
            x = [d.getLocation(i)[0] for i in range(pcount)]
            y = [d.getLocation(j)[1] for j in range(pcount)]
            z = [d.getLocation(k)[2] for k in range(pcount)]
            ax.scatter(x,y,z,alpha=0.5)
    plt.show()

if __name__ == '__main__':
    csv = 'test_rec30_dim3_pos3_rad2.csv'
    pcount = 3
    answer = input('Would you like to change the csv file? (Y/N)')
    if answer == 'Y':
        csv = input('Please specify the csv file name in data folder: ')
        pcount = int(input('Please input the probability count: '))
    datalist = batchImport(csv, pcount)
    visualize(datalist, pcount)