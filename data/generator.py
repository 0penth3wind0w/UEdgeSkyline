import os
import numpy as np
import random
from scipy.spatial import distance

# calculete distance between two points
# p1: list
# p2: list
def dist(p1, p2):
    dim = len(p1)
    if dim != len(p2):
        return -1
    else:
        return distance.euclidean(p1, p2)

# generate one data location accouding to dimension and bond
def datagen(dim, possibility, radius, bond=[0,100]):
    center = [random.randint(bond[0],bond[1]) for x in range(dim)]
    result = []
    for p in range(possibility):
        end = False
        while not end:
            location = [ i+random.randint(-1*radius,radius) for i in center ]
            if dist(location, center) < radius and location not in result:
                end = True
                result.append(location)
    return result

# generate csv file
def csvgen(path, count, dim, pcount, rad):
    with open(path+'/data_'+'rec'+str(count)+'_dim'+str(dim)+'_pos'+str(pcount)+'_rad'+str(rad)+'.csv', 'w') as data:
        for c in range(count):
            # generate probability outcome according to 'possibility'
            probs = np.random.dirichlet(np.ones(pcount),size=1).tolist()[0]
            # label
            data.write('d_'+str(c)+'; ')
            last = pcount - 1
            record = datagen(dim, pcount, rad, bond=[0+rad,100-rad])
            for i,p in enumerate(probs):
                if i == last:
                    data.write(str(p)+'; '+str(record[i])+'\n')
                else:
                    data.write(str(p)+'; '+str(record[i])+'; ')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    count = int(input('How many data is needed: '))
    dim = int(input('How many dimension of data: '))
    pcount = int(input('How many possible output of each data: '))
    rad = int(input('Radius of the record: '))
    csvgen(here, count, dim, pcount, rad)
    print("Done")
