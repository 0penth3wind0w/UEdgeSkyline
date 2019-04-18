import os
import numpy as np
import random
from scipy.stats import truncnorm
from scipy.spatial import distance

def dist(p1, p2):
    """
    Calculate the distance of two given points.

    :params p1: list(int)
    :params p2: list(int)
    """
    dim = len(p1)
    if dim != len(p2):
        return -1
    else:
        return distance.euclidean(p1, p2)

def datagen(dim, possibility, radius, center):
    """
    Genetate data instances according to given params.
    Return a list which contains locations according to possibility.
    
    :params dim: int
        Dimension of the data
    :params possibility: int
        Total instance count of a data record
    :params radius: int
        The parameter that bound all possible instance in a limited region.
        The function will generate a central point. The distance between generated instance location and the central point will not exceed this radius.
    :params center: list(int)
        The center point of data
    """
    result = []
    for p in range(possibility):
        end = False
        while not end:
            location = [ i+random.randint(-1*radius,radius) for i in center ]
            if location not in result:
                end = True
                result.append(location)
    return result

def csvgen(path, count, dim, pcount, rad, dmin, dmax):
    """
    Generate csv files accouding to params given.

    :params path: string
        The path of folder which the generated csv file is stored.
    :params count: int
        The number of data to be generated.
    :params dim: int
        The dimension of data.
    :params pcount: int
        Total instance count of a data record.
    :params rad: int
        Use to set the radius in datagen()
    :param dmin: int
        Data range minimum.
    :param dmax: int
        Data range maximum.
    """
    center_min = dmin+rad
    center_max = dmax-rad

    shmin, shmax, shavg = -(center_max-center_min)/2,(center_max-center_min)/2, (center_max+center_min)/2
    sc = int((center_max+center_min)/6)

    with open(path+'/norm'+str(count)+'_dim'+str(dim)+'_pos'+str(pcount)+'_rad'+str(rad)+'_'+str(dmin)+str(dmax)+'.csv', 'w') as data:
        
        for idx,c in enumerate(truncnorm(a=shmin/sc, b=shmax/sc, scale=sc).rvs(size=(count,dim))):
            # generate probability outcome according to 'possibility'
            probs = np.random.dirichlet(np.ones(pcount),size=1).tolist()[0]
            intc = [int(i) for i in c]
            # label
            data.write('d_'+str(idx)+'; ')
            last = pcount - 1
            record = datagen(dim, pcount, rad, intc)
            for i,p in enumerate(probs):
                if i == last:
                    data.write(str(p)+'; '+str([int(orid+shavg) for orid in record[i]])+'\n')
                else:
                    data.write(str(p)+'; '+str([int(orid+shavg) for orid in record[i]])+'; ')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    count = int(input('How many data is needed: '))
    dim = int(input('How many dimension of data: '))
    pcount = int(input('How many possible output of each data: '))
    rad = int(input('Radius of the record: '))
    dmin = int(input('Data range min: '))
    dmax = int(input('Data range max: '))
    csvgen(here, count, dim, pcount, rad, dmin, dmax)
    print("Done")
    

