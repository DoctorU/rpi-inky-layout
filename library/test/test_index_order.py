import unittest
from rpi_inky_layout import IndexOrder


class TestLayoutIndexCount(unittest.TestCase):

    def testIndexCount(self):
        self.assertEqual([0], IndexOrder.alternating(1))
        self.assertEqual([0, 1], IndexOrder.alternating(2))
        self.assertEqual([0, 2, 1], IndexOrder.alternating(3))
        self.assertEqual([0, 3, 1, 2], IndexOrder.alternating(4))
        self.assertEqual([0, 4, 1, 3, 2], IndexOrder.alternating(5))
        self.assertEqual([0, 5, 1, 4, 2, 3], IndexOrder.alternating(6))
        self.assertEqual([0, 6, 1, 5, 2, 4, 3], IndexOrder.alternating(7))


if __name__ == '__main__':
    unittest.main()
