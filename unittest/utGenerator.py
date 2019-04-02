import os, sys
sys.path.append(os.path.abspath(os.pardir))

import unittest
from data.generator import dist, datagen

class TestData(unittest.TestCase):
    def test_dist(self):
        p1 = [0,0]
        p2 = [3,4]
        self.assertEqual(dist(p1,p2), 5)
    def test_datagen(self):
        s = datagen(2,2,2,[0,100])
        self.assertLessEqual(dist(s[0],s[1]),4)

if __name__ == '__main__':
    unittest.main()