# No class implemented in this file. Test only.
import os, sys
sys.path.append(os.path.abspath(os.pardir))

from rtree import index
from data.dataClass import Data

if __name__ == '__main__':
    p = index.Property()
    p.dimension = 2
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    idx3d = index.Index('3d_index',properties=p)
    test = Data('t1',2)
    test.insertLocation(0.4,[6,4])
    test.insertLocation(0.6,[3,5])
    #               (d1min,d2min,...,dnmin,d1max,d2max,...,dnmax)
    # idx3d.insert(1, test.getMinMaxTuple(),obj=test)
    idx3d.insert(1, test.getMinMaxTuple(),obj=test)
    
    # idx3d.insert(1, (2, 60, 23, 4, 61, 25), obj='h1')
    # idx3d.insert(2, (2, 3, 22, 4, 5, 24),obj='h2')
    # idx3d.insert(3, (2, 51, 30, 4, 54, 31),obj='h3')
    # idx3d.insert(4, (2, 51, 23, 4, 65, 45),obj='h4')
    
    #                              (d1min,d2min,...,dnmin,d1max,d2max,...,dnmax)
    h = [i.object for i in (idx3d.intersection( (0,0,10,10) ,objects=True))]
    
    # h = list(idx3d.intersection( (0, 50, 22, 3, 62, 43) ,objects=True))
    
    for i in h:
        print(i)

    # for i in h:    
    #     print(i.object.getLabel())
    #     print(i.bbox)