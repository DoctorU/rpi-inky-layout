
import unittest
from rpi_inky_layout import Position


class TestLayoutRotation(unittest.TestCase):

    def testTopLeft(self):
        self.assertEqual((0, 0), Position.top_left((10, 10), (8, 8)))

    def testTopCentre(self):
        self.assertEqual((1, 0), Position.top_centre((10, 10), (8, 8)))

    def testTopRight(self):
        self.assertEqual((2, 0), Position.top_right((10, 10), (8, 8)))

    def testMiddleLeft(self):
        self.assertEqual((0, 1), Position.middle_left((10, 10), (8, 8)))

    def testMiddleCentre(self):
        self.assertEqual((1, 1), Position.middle_centre((10, 10), (8, 8)))

    def testMiddleRight(self):
        self.assertEqual((2, 1), Position.middle_right((10, 10), (8, 8)))

    def testBottomLeft(self):
        self.assertEqual((0, 2), Position.bottom_left((10, 10), (8, 8)))

    def testBottomCentre(self):
        self.assertEqual((1, 2), Position.bottom_centre((10, 10), (8, 8)))

    def testBottomRight(self):
        self.assertEqual((2, 2), Position.bottom_right((10, 10), (8, 8)))
