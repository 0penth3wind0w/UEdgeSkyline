# Test different data dimension
# Data: 1000 records, possible instance = 5, radius = 5
# Data: dimension from 2 to 10
# Sliding window = 300
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from data.dataClass import batchImport
from skyline.slideBPSky import slideBPSky
from skyline.slideUPSky import slideUPSky

def dim_time():
    print("=== Test how dimension of data affect running time ===")
    dim = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for d in dim:
        dqueue = batchImport('10000_dim'+str(d)+'_pos5_rad5_01000.csv', 5)
        print('========== Data dimension = '+ str(d) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = slideBPSky(d, 5, 5, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        tbsky.removeRtree()
        print("--- %s seconds ---" % (time.time() - start_time))
        print('---------- Update ----------')
        tusky = slideUPSky(d, 5, 5, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
        tusky.removeRtree()
        print("--- %s seconds ---" % (time.time() - start_time))

def dim_avgsk():
    print("=== Test how dimension of data affect candidate size ===")
    dim = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    dqueue = batchImport('10000_dim'+str(dim)+'_pos5_rad5_01000.csv', 5)
    for d in dim:
        print('========== Data dimension = '+ str(d) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = slideBPSky(d, 5, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
            avgsk1 += len(tbsky.getSkyline())
            avgsk2 += len(tbsky.getSkyline2())
        tbsky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))
        print('---------- Update ----------')
        tusky = slideUPSky(d, 5, 5, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
            avgsk1 += len(tusky.getSkyline())
            avgsk2 += len(tusky.getSkyline2())
        tusky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))

if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        dim_time()
    elif switch == 2: # test avg sky
        dim_avgsk()
    elif switch == 3:
        dim_time()
        dim_avgsk()
    else:
        print('error')
