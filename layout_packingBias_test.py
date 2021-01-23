#!/usr/bin/env python3
from Layout import Layout
import unittest
from PIL import Image, ImageDraw

 
class TestLayoutPackingBias(unittest.TestCase):

    def test_getChildPackingBiasTotalAndBiasStart(self):
        print("*** ** test_getChildPackingBiasTotalAndBiasStart")
        layout = Layout((100,100))
        self.assertEqual(0, layout._getChildrenPackingBiasTotal())

        layout.addLayer(packingBias=3)
        self.assertEqual(3, layout._getChildrenPackingBiasTotal())

        layout.addLayer(packingBias=3)
        self.assertEqual(6, layout._getChildrenPackingBiasTotal())

        self.assertEqual(0, layout._getChildPackingBiasStart(0))
        self.assertEqual(3, layout._getChildPackingBiasStart(1))
        print("END OF test_getChildPackingBiasTotalAndBiasStart")

    def testLayoutWidthHorizontal(self):
        print("*** ** testLayoutWidthHorizontal")
        layout = Layout((200, 10), packingMode='h', border=(0,0))
        layout1 = layout.addLayer(packingBias=3)
        self.assertEqual(200, layout1.size[0])

        layout2 = layout.addLayer(packingBias=1)

        self.assertEqual(150, layout1.size[0])
        self.assertEqual(50, layout2.size[0])
        self.assertEqual((0,0), layout1.topleft)
        self.assertEqual((150,0), layout2.topleft)
        layout.write("test/expected-images/testLayoutWidthHorizontal.png")
        print ("END OF testLayoutWidthHorizontal")

    def testLayoutWidthVertical(self):
        print("*** ** testLayoutWidthVertical")

        layout = Layout((10, 200), packingMode='v')
        layout1 = layout.addLayer(packingBias=3)
        self.assertEqual(200, layout1.size[1])

        layout2 = layout.addLayer(packingBias=1)

        self.assertEqual(150, layout1.size[1])
        self.assertEqual(50, layout2.size[1])
        self.assertEqual((0,0), layout1.topleft)
        self.assertEqual((0,150), layout2.topleft)
        layout.write("test/expected-images/testLayoutWidthVertical.png")
        print ("END OF testLayoutWidthVertical")

    def testWrite(self):
        print("*** ** testWrite")
        layout = Layout((200,200))
        layout1 = layout.addLayer(packingBias=1)
        layout2 = layout.addLayer(packingBias=3)

        def writeImage(layout, colour, text):
            img = Image.new("RGB", layout.size, colour)
            draw = ImageDraw.Draw(img)
            draw.text((0,0), text)
            layout.setImage(img)

        writeImage(layout1, 0xff0000, "layout1")
        writeImage(layout2, 0x0088ff, "layout2")
        writeImage(layout, 0x000000, "layout")
        layout.write("test/expected-images/test-packingBias.png")
        print("END OF testWrite")

if __name__ == '__main__':
    unittest.main()
