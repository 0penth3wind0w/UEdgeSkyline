import os, sys
sys.path.append(os.path.abspath(os.pardir))

import unittest
from data.dataClass import Data
from dominate import dominateProbability ,dominateStat

class TestDominate(unittest.TestCase):
    def test_dominateProbability1(self):
        tData1 = Data("t_1",2)
        tData1.insertLocation(0.5, [8,2])
        tData1.insertLocation(0.5, [4,8])
        tData2 = Data("t_2",2)
        tData2.insertLocation(0.3, [7,9])
        tData2.insertLocation(0.4, [2,4])
        self.assertEqual(dominateProbability(tData1,tData2), 0.15)
    def test_dominateProbability2(self):
        tData3 = Data("t_3",2)
        tData3.insertLocation(0.2, [1,3,5])
        tData3.insertLocation(0.8, [2,4,5])
        tData4 = Data("t_4",2)
        tData4.insertLocation(0.4, [2,4,6])
        tData4.insertLocation(0.6, [1,5,7])
        self.assertEqual(dominateProbability(tData3,tData4), 0.52)
    
    def test_dominateStat1(self):
        tLocation1 = [0.5, [2,5]]
        tLocation2 = [0.3, [1,4]]
        self.assertEqual(dominateStat(tLocation1[1],tLocation2[1]), False)
    def test_dominateStat2(self):
        tLocation1 = [0.2, [2,3]]
        tLocation2 = [0.3, [1,4]]
        self.assertEqual(dominateStat(tLocation1[1],tLocation2[1]), None)
    def test_dominateStat3(self):
        tLocation1 = [0.4, [2,2]]
        tLocation2 = [0.3, [3,3]]
        self.assertEqual(dominateStat(tLocation1[1],tLocation2[1]), True)
    
if __name__ == '__main__':
    unittest.main()