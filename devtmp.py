
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
data = batchImport('20_dim2_pos5_rad5_0100.csv', 5)

fig = plt.figure()
ax = fig.add_subplot(111)

for d in data:
    x = [d.getLocation(i)[0] for i in range(5)]
    y = [d.getLocation(j)[1] for j in range(5)]
    ax.scatter(x,y,alpha=0.5)
    ax.add_patch(Rectangle(xy=(d.getLocationMin()[0],d.getLocationMin()[1]),width=d.getLocationMax()[0]-d.getLocationMin()[0], height=d.getLocationMax()[1]-d.getLocationMin()[1], linewidth=1, fill=False))    

plt.show()

# for i in range(100):
#     test.receiveData(dqueue[i])
#     test.updateSkyline()
#     if i == 51 or i== 52 or i== 53 or i== 54 or i== 55:
#         print("Window: "+str(len(test.getWindow())))
#         print("Sk: "+ str(len(test.getSkyline())))
#         # for each in test.getSkyline():
#         #     print(each)
#         print("Sk2: "+ str(len(test.getSkyline2())))
#         visualize(test.getWindow(), 5, [0,100])
#         visualize(test.getSkyline(), 5, [0,100])
#         visualize(test.getSkyline2(), 5, [0,100])
#         print()
# test.removeRtree()



