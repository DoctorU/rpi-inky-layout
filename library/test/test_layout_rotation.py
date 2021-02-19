from PIL import Image, ImageDraw
import numpy
import unittest

from rpi_inky_layout import Layout, Rotation
from . import layout_fixtures as fixtures


class TestLayoutRotation(unittest.TestCase):

    @staticmethod
    def writeImage(layout, filename):
        layout.write('test/expected-images/' + filename)

    def testRotation(self):
        self.assertEqual(0, Rotation.UP.value)
        self.assertEqual(1, Rotation.RIGHT.value)
        self.assertEqual(3, Rotation.LEFT.value)
        self.assertEqual(2, Rotation.DOWN.value)

    def testCreateLayoutRotatedUp(self):
        layout = Layout((200, 100), rotation=Rotation.UP)
        self.assertEqual((200, 100), layout.size)
        self.assertEqual(0, layout.rotation_degrees)

    def testCreateLayoutRotatedLeft(self):
        layout = Layout((200, 100), rotation=Rotation.LEFT)
        self.assertEqual((100, 200), layout.size)
        self.assertEqual(270, layout.rotation_degrees)

    def testCreateLayoutRotatedDown(self):
        layout = Layout((200, 100), rotation=Rotation.DOWN)
        self.assertEqual((200, 100), layout.size)
        self.assertEqual(180, layout.rotation_degrees)

    def testCreateLayoutRotatedRight(self):
        layout = Layout((200, 100), rotation=Rotation.RIGHT)
        self.assertEqual((100, 200), layout.size)
        self.assertEqual(90, layout.rotation_degrees)

    def testLayoutRotatedRightAdd3Layers(self):
        self.add3LayersAndRotate((300, 100), Rotation.RIGHT)

    def testLayoutRotatedLeftAdd3Layers(self):
        self.add3LayersAndRotate((300, 100), Rotation.LEFT)

    def testLayoutRotatedDownAdd3Layers(self):
        self.add3LayersAndRotate((100, 300), Rotation.DOWN)

    def testLayoutRotatedUpAdd3Layers(self):
        self.add3LayersAndRotate((100, 300), Rotation.UP)

    def add3LayersAndRotate(self, size, rotation):
        layout = fixtures.threeLayers(
            size, packingMode='v', border=0, rotation=rotation
        )
        img = Image.new("RGB", layout.size, 0x000)
        layout.setImage(img)
        [
            self.assertEqual((100, 100), child.size)
            for child
            in layout.children
        ]

        layout1 = layout.children[0]
        layout2 = layout.children[1]
        layout3 = layout.children[2]
        self.assertEqual((0, 0), layout1.topLeft)
        self.assertEqual((0, 100), layout2.topLeft)
        self.assertEqual((0, 200), layout3.topLeft)
        img1 = Image.new("RGB", layout1.size, 0xff8800)  # red
        self.drawTextOnImage("layout1", img1)
        layout1.setImage(img1)
        img2 = Image.new("RGB", layout2.size, 0x000ff00)  # green
        self.drawTextOnImage("layout2", img2)
        layout2.setImage(img2)
        img3 = Image.new("RGB", layout3.size, 0xaaaaff)  # blue
        self.drawTextOnImage("layout3", img3)
        layout3.setImage(img3)
        self.writeImage(
            layout,
            "test-rotated-{rot}-add-3-layers.png".format(rot=rotation.name)
        )

    def drawTextOnImage(self, text, img):
        draw = ImageDraw.Draw(img)
        tsize = draw.textsize(text)
        tdiff = numpy.subtract(img.size, tsize)
        thalf = numpy.divide(tdiff, 2)
        tpos = tuple(thalf)

        draw.text(tpos, text, 0x000000)


if __name__ == '__main__':
    unittest.main()
