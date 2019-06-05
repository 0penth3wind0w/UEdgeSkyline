
# Sliding window update PSky
from skyline.PSky import PSky
from data.dataClass import Data, batchImport
from visualize.visualize import visualize

import random

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from data.dataClass import Data, batchImport
from skyline.slideUPSky import slideUPSky

test = slideUPSky(2, 5, 4, [0,100], wsize=10)
dqueue = batchImport('100_dim2_pos5_rad4_0100.csv', 5)

for i in range(100):
    test.receiveData(dqueue[i])
    test.updateSkyline()
    if i == 51 or i== 52 or i== 53 or i== 54 or i== 55:
        print("Window: "+str(len(test.getWindow())))
        print("Sk: "+ str(len(test.getSkyline())))
        # for each in test.getSkyline():
        #     print(each)
        print("Sk2: "+ str(len(test.getSkyline2())))
        visualize(test.getWindow(), 5, [0,100])
        visualize(test.getSkyline(), 5, [0,100])
        visualize(test.getSkyline2(), 5, [0,100])
        print()
test.removeRtree()