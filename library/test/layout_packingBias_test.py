#!/usr/bin/env python3
from PIL import Image, ImageDraw
import unittest

from rpi_inky_layout import Layout


class TestLayoutPackingBias(unittest.TestCase):

    @staticmethod
    def writeImage(layout, filename):
        layout.write('test/expected-images/' + filename)

    def test_getChildPackingBiasTotalAndBiasStart(self):
        layout = Layout((100, 100))
        self.assertEqual(0, layout._getChildrenPackingBiasTotal())

        layout.addLayer(packingBias=3)
        self.assertEqual(3, layout._getChildrenPackingBiasTotal())

        layout.addLayer(packingBias=3)
        self.assertEqual(6, layout._getChildrenPackingBiasTotal())

        self.assertEqual(0, layout._getChildPackingBiasStart(0))
        self.assertEqual(3, layout._getChildPackingBiasStart(1))

    def testLayoutWidthHorizontal(self):
        layout = Layout((200, 10), packingMode='h', border=(0, 0))
        layout1 = layout.addLayer(packingBias=3)
        self.assertEqual(200, layout1.size[0])

        layout2 = layout.addLayer(packingBias=1)

        self.assertEqual(150, layout1.size[0])
        self.assertEqual(50, layout2.size[0])
        self.assertEqual((0, 0), layout1.topleft)
        self.assertEqual((150, 0), layout2.topleft)
        self.writeImage(layout, "testLayoutWidthHorizontal.png")

    def testLayoutWidthVertical(self):

        layout = Layout((10, 200), packingMode='v')
        layout1 = layout.addLayer(packingBias=3)
        self.assertEqual(200, layout1.size[1])

        layout2 = layout.addLayer(packingBias=1)

        self.assertEqual(150, layout1.size[1])
        self.assertEqual(50, layout2.size[1])
        self.assertEqual((0, 0), layout1.topleft)
        self.assertEqual((0, 150), layout2.topleft)
        self.writeImage(layout, "testLayoutWidthVertical.png")

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
