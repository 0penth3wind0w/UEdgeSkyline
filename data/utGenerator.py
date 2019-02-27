import unittest
from generator import dimgen

class TestData(unittest.TestCase):
    def test_dimgen_dimension(self):
        case1 = dimgen(3)
        self.assertEqual(len(case1), 3)

if __name__ == '__main__':
    unittest.main()