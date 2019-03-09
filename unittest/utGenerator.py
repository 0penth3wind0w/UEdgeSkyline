import os, sys
sys.path.append(os.path.abspath(os.pardir))

import unittest
from data.generator import dist

class TestData(unittest.TestCase):
    def test_dist(self):
        d = dist([1,1],[4,5])
        self.assertEqual(d, 5)

if __name__ == '__main__':
    unittest.main()