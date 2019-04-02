import os, sys
sys.path.append(os.path.abspath(os.pardir))

import unittest
from data.dataClass import Data, batchImport

class TestData(unittest.TestCase):
    def test_Data_insertLocation(self):
        d_til = Data('d_til',1)
        d_til.insertLocation(1,[2,3,4])
        self.assertEqual(d_til.getLocation(0),[2,3,4])
    def test_Data_getLabel(self):
        d_gl = Data('d_gl', 2)
        self.assertEqual(d_gl.getLabel(),'d_gl')
    def test_Data_getPCount(self):
        d_gpc = Data('d_gpc',2)
        d_gpc.insertLocation(0.2,[2,3])
        d_gpc.insertLocation(0.8,[5,4])
        self.assertEqual(d_gpc.getPCount(),2)
    def test_Data_getProbLocSet(self):
        d_gpls = Data('d_gpls', 1)
        d_gpls.insertLocation(1, [4,4])
        self.assertEqual(d_gpls.getProbLocSet(0), [1,[4,4]])
        self.assertEqual(d_gpls.getProbLocSet(1), [None,[]])
    def test_Data_getProb(self):
        d_gp = Data('d_gp', 3)
        d_gp.insertLocation(0.1, [3,5])
        d_gp.insertLocation(0.4, [4,6])
        d_gp.insertLocation(0.5, [8,7])
        self.assertEqual(d_gp.getProb(0), 0.1)
        self.assertEqual(d_gp.getProb(1), 0.4)
        self.assertEqual(d_gp.getProb(2), 0.5)
        self.assertEqual(d_gp.getProb(3), None)
    def test_Data_getLocation(self):
        d_glo = Data('d_glo',2)
        d_glo.insertLocation(0.7, [3,6,2])
        d_glo.insertLocation(0.3, [4,1,8])
        self.assertEqual(d_glo.getLocation(0), [3,6,2])
        self.assertEqual(d_glo.getLocation(1), [4,1,8])
        self.assertEqual(d_glo.getLocation(2), [])
    def test_Data_getLocationMax(self):
        d_glm = Data('d_glm', 3)
        d_glm.insertLocation(0.2, [4,5,9])
        d_glm.insertLocation(0.2, [6,2,3])
        d_glm.insertLocation(0.2, [7,0,5])
        self.assertEqual(d_glm.getLocationMax(), [7,5,9])
    def test_Data_getLocationMin(self):
        d_glmi = Data('d_glmi', 3)
        d_glmi.insertLocation(0.2, [4,5,9])
        d_glmi.insertLocation(0.2, [6,2,3])
        d_glmi.insertLocation(0.2, [7,0,5])
        self.assertEqual(d_glmi.getLocationMin(), [4,0,3])
    def test_Data_getMinMaxTuple(self):
        d_gmmt = Data('d_gmmt',2)
        d_gmmt.insertLocation(0.7, [8,3,9])
        d_gmmt.insertLocation(0.3, [4,7,2])
        self.assertEqual(d_gmmt.getMinMaxTuple(), (4,3,2,8,7,9))

    def test_batchImport(self):
        output = batchImport('test_30_dim3_pos3_rad2_0100.csv',3)
        self.assertEqual(len(output), 30)
        psum = output[0].getProb(0) + output[0].getProb(1) + output[0].getProb(2)
        self.assertAlmostEqual(psum, 1)
        self.assertEqual(output[2].getLocation(4), [])
if __name__ == '__main__':
    unittest.main()