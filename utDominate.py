import os
import unittest
from dataClass import Data
from dominate import dominateProbability ,dominateStat

here = os.path.dirname(os.path.abspath(__file__))

class TestDominate(unittest.TestCase):
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
    def test_dominateProbability(self):
        # tData1 = Data("t_1",2)
        # tData1.insertLocation(0.5, [6,2])
        # tData1.insertLocation(0.5, [4,8])
        # tData2 = Data("t_2",2)
        # tData2.insertLocation(0.3, [7.9])
        # tData2.insertLocation(0.4, [2,4])

        # self.assertEqual(dominateProbability(tData1,tData2), 0)

if __name__ == '__main__':
    unittest.main()