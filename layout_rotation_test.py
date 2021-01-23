#!/usr/bin/env python3
from Layout import Rotation
from math import floor
from Layout import Layout
from random import randint
import unittest
from PIL import Image, ImageDraw

import numpy

class TestLayoutRotation(unittest.TestCase):

    def writeToFile(self, layout, filename):
        layout.write(filename
        )

    def testRotation(self):
        self.assertEqual(0, Rotation.UP.value)
        self.assertEqual(1, Rotation.RIGHT.value)
        self.assertEqual(3, Rotation.LEFT.value)
        self.assertEqual(2, Rotation.DOWN.value)

    def testCreateLayoutRotatedUp(self):
        l = Layout((200,100), rotation=Rotation.UP)
        self.assertEqual((200,100), l.size)
        self.assertEqual(0, l.rotation_degrees)

    def testCreateLayoutRotatedLeft(self):
        l = Layout((200,100), rotation=Rotation.LEFT)
        self.assertEqual((100,200), l.size)
        self.assertEqual(270, l.rotation_degrees)

    def testCreateLayoutRotatedDown(self):
        l = Layout((200,100), rotation=Rotation.DOWN)
        self.assertEqual((200,100), l.size)
        self.assertEqual(180, l.rotation_degrees)

    def testCreateLayoutRotatedRight(self):
        l = Layout((200,100), rotation=Rotation.RIGHT)
        self.assertEqual((100,200), l.size)
        self.assertEqual(90, l.rotation_degrees)

    def testLayoutRotatedRightAdd3Layers(self):
        self.add3LayersAndRotate((300,100), Rotation.RIGHT)

    def testLayoutRotatedLeftAdd3Layers(self):
        self.add3LayersAndRotate((300,100), Rotation.LEFT)

    def testLayoutRotatedDownAdd3Layers(self):
        self.add3LayersAndRotate((100,300), Rotation.DOWN)

    def testLayoutRotatedUpAdd3Layers(self):
        self.add3LayersAndRotate((100,300), Rotation.UP)

    def add3LayersAndRotate(self, size,  rotation):
        l = Layout (size, packingMode='v', border=0, rotation=rotation)
        l1 = l.addLayer()
        l2 = l.addLayer()
        l3 = l.addLayer()
        img = Image.new("RGB", l.size, 0x000)
        l.setImage(img)
        self.assertEqual((100,100), l1.size)
        self.assertEqual((0,0), l1.topleft)
        self.assertEqual((100,100), l2.size)
        self.assertEqual((0,100), l2.topleft)
        self.assertEqual((100,100), l3.size)
        self.assertEqual((0,200), l3.topleft)
        img1 = Image.new("RGB", l1.size, 0xff0000) #red
        self.drawTextOnImage("l1", img1)
        l1.setImage(img1)
        img2 = Image.new("RGB", l2.size, 0x000ff00) # green
        self.drawTextOnImage("l2", img2)
        l2.setImage(img2)
        img3 = Image.new("RGB", l3.size, 0x0000ff) # blue
        self.drawTextOnImage("l3", img3)
        l3.setImage(img3)
        l.write("test/expected-images/test-rotated-{rot}-add-3-layers.png".format(rot=rotation.name))

    def drawTextOnImage(self, text, img):
        draw = ImageDraw.Draw(img)
        tsize = draw.textsize(text)
        tdiff = numpy.subtract(img.size, tsize)
        thalf = numpy.divide(tdiff, 2)
        tpos = tuple(thalf)

        draw.text(tpos, text, 0x000000)

if __name__ == '__main__':
    unittest.main()
