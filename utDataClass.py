import os
import unittest
from dataClass import Data, batchImport

here = os.path.dirname(os.path.abspath(__file__))

class TestData(unittest.TestCase):
    def test_batchImport(self):
        output333 = batchImport('test_3r3d3p.csv',3)
        self.assertEqual(len(output333), 3)
        psum = output333[0].getLocation(0)[0] + output333[0].getLocation(1)[0] + output333[0].getLocation(2)[0]
        self.assertAlmostEqual(psum, 1)
        self.assertEqual(output333[2].getLocation(4), [])
    def test_Data_getPCount(self):
        tData = Data("t1",2)
        tData.insertLocation(0.2,[2,3])
        tData.insertLocation(0.8,[5,4])
        self.assertEqual(tData.getPCount(),2)
    
if __name__ == '__main__':
    unittest.main()