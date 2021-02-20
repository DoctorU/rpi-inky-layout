#!/usr/bin/env python3
from PIL import Image, ImageDraw
import unittest

from rpi_inky_layout import Layout


class TestLayoutPackingBias(unittest.TestCase):

    @staticmethod
    def writeImage(layout, filename):
        layout.write('test/expected-images/' + filename)

    def test_getChildSlotTotalAndBiasStart(self):
        layout = Layout((100, 100))
        self.assertEqual(0, layout._getChildSlotTotal())

        layout.addLayer(packingBias=3)
        self.assertEqual(3, layout._getChildSlotTotal())

        layout.addLayer(packingBias=3)
        self.assertEqual(6, layout._getChildSlotTotal())

        self.assertEqual(0, layout._getChildSlotStart(0))
        self.assertEqual(3, layout._getChildSlotStart(1))

    def testPackingBiasHorizontal(self):
        layout = Layout((200, 10), packingMode='h', border=(0, 0))
        layout1 = layout.addLayer(packingBias=3)
        self.assertEqual((200, 10), layout1.size)

        layout2 = layout.addLayer(packingBias=1)

        self.assertEqual((150, 10), layout1.size)
        self.assertEqual((50, 10), layout2.size)
        self.assertEqual((0, 0), layout1.topLeft)
        self.assertEqual((150, 0), layout2.topLeft)
        self.writeImage(layout, "testPackingBiasHorizontal.png")

    def testPackingBiasVertical(self):

        layout = Layout((10, 200), packingMode='v', border=(0, 0))
        layout1 = layout.addLayer(packingBias=3)
        self.assertEqual((10, 200), layout1.size)

        layout2 = layout.addLayer(packingBias=1)

        self.assertEqual((10, 150), layout1.size)
        self.assertEqual((10, 50), layout2.size)
        self.assertEqual((0, 0), layout1.topLeft)
        self.assertEqual((0, 150), layout2.topLeft)
        self.writeImage(layout, "testPackingBiasVertical.png")

    def testWrite(self):
        layout = Layout((200, 200))
        layout1 = layout.addLayer(packingBias=1)
        layout2 = layout.addLayer(packingBias=3)

        def setImage(layout, colour, text):
            img = Image.new("RGB", layout.size, colour)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), text)
            layout.setImage(img)

        setImage(layout1, 0xff0000, "layout1")
        setImage(layout2, 0x0088ff, "layout2")
        setImage(layout, 0x000000, "layout")
        self.writeImage(layout, "test-packingBias.png")


if __name__ == '__main__':
    unittest.main()
