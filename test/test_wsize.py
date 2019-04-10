# Test different sliding window size
# Data: 1000 records, 2D, possible instance = 5, radius = 5
# Sliding window from 100 to 1000, increase by 100
import os, sys
sys.path.append(os.path.abspath(os.pardir))

import time

from data.dataClass import batchImport
from skyline.slideBPSky import slideBPSky
from skyline.slideUPSky import slideUPSky

def wsize_time():
    print("=== Test how window size affect running time ===")
    wsize = [100,200,300,400,500,600,700,800,900,1000]
    dqueue = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    for w in wsize:
        print('========== window size = '+ str(w) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = slideBPSky(2, 5, 5, [0,1000], wsize=w)
        start_time = time.time()
        for i in range(10000):
            tbsky.receiveData(dqueue[i])
            tbsky.updateSkyline()
        tbsky.removeRtree()
        print("--- %s seconds ---" % (time.time() - start_time))
        print('---------- Update ----------')
        tusky = slideUPSky(2, 5, 5, [0,1000], wsize=w)
        start_time = time.time()
        for i in range(10000):
            tusky.receiveData(dqueue[i])
            tusky.updateSkyline()
        tusky.removeRtree()
        print("--- %s seconds ---" % (time.time() - start_time))

def wsize_avgsk():
    print("=== Test how window size affect candidate skyline ===")
    wsize = [100,200,300,400,500,600,700,800,900,1000]
    dqueue = batchImport('10000_dim2_pos5_rad5_01000.csv', 5)
    for w in wsize:
        print('========== window size = '+ str(w) + ' ==========\n')
        print('---------- Brute force ----------')
        tbsky = slideBPSky(2, 5, 5, [0,1000], wsize=w)
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
        tusky = slideUPSky(2, 5, 5, [0,1000], wsize=w)
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
        wsize_time()
    elif switch == 2: # test avg sky
        wsize_avgsk()
    elif switch == 3:
        wsize_time()
        wsize_avgsk()
    else:
        print('error')
