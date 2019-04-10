# Test different radius
# Data: 1000 records, 2D, instance = 5
# Data: radius from 3 to 10
# Sliding window = 300

import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from data.dataClass import batchImport
from skyline.slideBPSky import slideBPSky
from skyline.slideUPSky import slideUPSky

def radius_time():
    print('=== Test how data radius affect running time ===')
    radius = [3, 4, 5, 6, 7, 8, 9, 10]
    for r in radius:
        dqueue = batchImport('10000_dim2_pos5_rad'+str(r)+'01000.csv', 5)
        print('========== radius = '+ str(r) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = slideBPSky(2, 5, r, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        tbsky.removeRtree()
        print("--- %s seconds ---" % (time.time() - start_time))
        print('---------- Update ----------')
        tusky = slideUPSky(2, 5, r, [0,1000], wsize=300)
        start_time = time.time()
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
        tusky.removeRtree()
        print("--- %s seconds ---" % (time.time() - start_time))

def radius_avgsk():
    print('=== Test how data radius affect candidate skyline ===')
    radius = [3, 4, 5, 6, 7, 8, 9, 10]
    for r in radius:
        dqueue = batchImport('10000_dim2_pos5_rad'+str(r)+'01000.csv', 5)
        print('========== radius = '+ str(r) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = slideBPSky(2, 5, r, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
            avgsk1 += len(tusky.getSkyline())
            avgsk2 += len(tusky.getSkyline2())
        tbsky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))
        print('---------- Update ----------')
        tusky = slideUPSky(2, 5, r, [0,1000], wsize=300)
        avgsk1, avgsk2 = 0, 0
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
            avgsk1 += len(tusky.getSkyline())
            avgsk2 += len(tusky.getSkyline2())
        tbsky.removeRtree()
        avgsk1, avgsk2 = avgsk1/10000, avgsk2/10000
        print('Avg. sky1: '+ str(avgsk1))
        print('Avg. sky2: '+ str(avgsk2))

if __name__ == '__main__':
    print("1: Test time\n2: Test average skyline size \n3: Run all test")
    switch = int(input('Choose your test: '))
    if switch == 1: # test time
        radius_time()
    elif switch == 2: # test avg sky
        radius_avgsk()
    elif switch == 3:
        radius_time()
        radius_avgsk()
    else:
        print('error')