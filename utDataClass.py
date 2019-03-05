import os
import unittest
from dataClass import Data, batchImport

here = os.path.dirname(os.path.abspath(__file__))

class TestData(unittest.TestCase):
    def test_batchImport(self):
        output333 = batchImport('test_3r3d3p.csv',3)
        self.assertEqual(len(output333), 3)
        psum = output333[0].getProb(0) + output333[0].getProb(1) + output333[0].getProb(2)
        self.assertAlmostEqual(psum, 1)
        self.assertEqual(output333[2].getLocation(4), [])
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
    
if __name__ == '__main__':
    unittest.main()