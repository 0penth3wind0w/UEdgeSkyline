import random
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from data.dataClass import Data, batchImport

data = batchImport('20_dim2_pos5_rad5_0100.csv', 5)

fig = plt.figure()
ax = fig.add_subplot(111)

for d in data:
    x = [d.getLocation(i)[0] for i in range(5)]
    y = [d.getLocation(j)[1] for j in range(5)]
    ax.scatter(x,y,alpha=0.5)
    ax.add_patch(Rectangle(xy=(d.getLocationMin()[0],d.getLocationMin()[1]),width=d.getLocationMax()[0]-d.getLocationMin()[0], height=d.getLocationMax()[1]-d.getLocationMin()[1], linewidth=1, fill=False))    

plt.show()