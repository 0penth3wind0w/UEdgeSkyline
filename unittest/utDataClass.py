import os, sys
sys.path.append(os.path.abspath(os.pardir))

import unittest
from data.dataClass import Data, batchImport

class TestData(unittest.TestCase):
    def test_batchImport(self):
        output = batchImport('test_rec5_dim3_pos3_rad2.csv',3)
        self.assertEqual(len(output), 5)
        psum = output[0].getProb(0) + output[0].getProb(1) + output[0].getProb(2)
        self.assertAlmostEqual(psum, 1)
        self.assertEqual(output[2].getLocation(4), [])
    def test_Data_getLabel(self):
        tData1 = Data('t1', 2)
        self.assertEqual(tData1.getLabel(),'t1')
    def test_Data_getPCount(self):
        tData2 = Data('t2',2)
        tData2.insertLocation(0.2,[2,3])
        tData2.insertLocation(0.8,[5,4])
        self.assertEqual(tData2.getPCount(),2)
    def test_Data_getProbLocSet(self):
        tData3 = Data('t3', 1)
        tData3.insertLocation(1, [4,4])
        self.assertEqual(tData3.getProbLocSet(0), [1,[4,4]])
        self.assertEqual(tData3.getProbLocSet(1), [None,[]])
    def test_Data_getProb(self):
        tData4 = Data('t4', 3)
        tData4.insertLocation(0.1, [3,5])
        tData4.insertLocation(0.4, [4,6])
        tData4.insertLocation(0.5, [8,7])
        self.assertEqual(tData4.getProb(0), 0.1)
        self.assertEqual(tData4.getProb(1), 0.4)
        self.assertEqual(tData4.getProb(2), 0.5)
        self.assertEqual(tData4.getProb(3), None)
    def test_Data_getLocation(self):
        tData5 = Data('t5',2)
        tData5.insertLocation(0.7, [3,6,2])
        tData5.insertLocation(0.3, [4,1,8])
        self.assertEqual(tData5.getLocation(0), [3,6,2])
        self.assertEqual(tData5.getLocation(1), [4,1,8])
        self.assertEqual(tData5.getLocation(2), [])
    def test_Data_getLocationMax(self):
        tData6 = Data('t6', 3)
        tData6.insertLocation(0.2, [4,5,9])
        tData6.insertLocation(0.2, [6,2,3])
        tData6.insertLocation(0.2, [7,0,5])
        self.assertEqual(tData6.getLocationMax(), [7,5,9])
    
if __name__ == '__main__':
    unittest.main()