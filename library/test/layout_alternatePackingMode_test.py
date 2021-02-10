#!/usr/bin/env python3
from PIL import Image, ImageDraw
import unittest

from rpi_inky_layout import Layout


class TestLayoutAlternatePackingMode(unittest.TestCase):

    @staticmethod
    def writeImage(layout, filename):
        layout.write('test/expected-images/' + filename)

    def test_getChildSlotTotalAndBiasStart(self):
        layout = Layout((100, 100))
        self.assertEqual(0, layout._getChildSlotTotal())

        layout1 = layout.addLayer(packingMode='h')
        self.assertEqual(1, layout._getChildSlotTotal())
        self.assertEqual((100, 100), layout.size)
        self.assertEqual((100, 100), layout1.size)

        layout11 = layout1.addLayer()
        layout12 = layout1.addLayer()
        self.assertEqual((100, 100), layout.size)
        self.assertEqual((100, 100), layout1.size)
        self.assertEqual((50, 100), layout11.size)
        self.assertEqual((50, 100), layout12.size)

        layout2 = layout.addLayer(packingMode='v')
        self.assertEqual((100, 100), layout.size)
        self.assertEqual((50, 100), layout1.size)
        self.assertEqual((50, 100), layout2.size)
        self.assertEqual((25, 100), layout11.size)
        self.assertEqual((25, 100), layout12.size)

        layout21 = layout2.addLayer()
        layout22 = layout2.addLayer()

        self.assertEqual((100, 100), layout.size)
        self.assertEqual((50, 100), layout1.size)
        self.assertEqual((25, 100), layout11.size)
        self.assertEqual((25, 100), layout12.size)
        self.assertEqual((50, 100), layout2.size)
        self.assertEqual((50, 50), layout21.size)
        self.assertEqual((50, 50), layout22.size)
        layouts = (layout11, layout12, layout21, layout22)
        [
            self._setImage(layout, (0x40*index, 0xff, 0xff), str(layout._id))
            for index, layout in enumerate(layouts)
        ]
        self.writeImage(layout, "test-alternatePackingMode.png")

    def _setImage(self, layout, colour, text):
        img = Image.new("HSV", layout.size, colour)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text)
        layout.setImage(img)


if __name__ == '__main__':
    unittest.main()
