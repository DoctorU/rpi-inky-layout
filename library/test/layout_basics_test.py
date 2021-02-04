from PIL import Image, ImageDraw
from random import randint
import unittest

from rpi_inky_layout import Layout


class TestLayoutBasics(unittest.TestCase):

    @staticmethod
    def writeToFile(layout, filename):
        layout.write('test/expected-images/' + filename)

    def testCreateLayout(self):
        layout = Layout((200, 100))
        self.assertEqual((200, 100), layout.size)

        filename = 'testCreateLayout1.png'
        img = self.NewImage(layout)
        draw = ImageDraw.Draw(img)
        draw.text((2, 50), filename)
        layout.setImage(img)
        self.writeToFile(layout, filename)

    def testAdd2ChildrenHorizontalPacking(self):
        layout = Layout((200, 100), 'h', border=2)
        img = self.NewImage(layout)
        draw = self.NewDraw(img)
        draw.text((2, 50), "main layout 1", 2)
        layout.setImage(img)
        layer1 = layout.addLayer()

        img = self.NewImage(layer1)
        draw = self.NewDraw(img)
        draw.text((2, 50), "layer 1-1", 2)
        layer1.setImage(img)

        self.assertEqual((196, 96), layer1.size)
        self.writeToFile(layer1, 'test2.png')

        layer2 = layout.addLayer()
        img = self.NewImage(layer2)
        draw = self.NewDraw(img)
        draw.text((2, 50), "layer 1-2", 2)
        layer2.setImage(img)

        self.assertEqual((97, 96), layer1.size)
        self.assertEqual((97, 96), layer2.size)
        self.writeToFile(layer2, 'test3.png')

    def testAdd2ChildrenVerticalPacking(self):
        layout = Layout((200, 100), 'v')

        layer1 = layout.addLayer()
        self.assertEqual((200, 100), layer1.size)

        layer2 = layout.addLayer()
        self.assertEqual((200, 50), layer1.size)
        self.assertEqual((200, 50), layer2.size)

    def testAddChildrenPackedVWithBorderEnabled(self):
        layout = Layout((200, 300), 'v', 1)
        layer1 = layout.addLayer()
        self.assertEqual((198, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 148), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 99), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 74), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 59), layer1.size)

    def testAddChildrenPackedHWithBorderEnabled(self):
        layout = Layout((200, 300), 'h', 1)
        layer1 = layout.addLayer()
        self.assertEqual((198, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((98, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((65, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((49, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((39, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((32, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((27, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((24, 298), layer1.size)

    def testTestGenerating2Layers(self):
        layout = Layout((400, 100), 'h', border=3)
        self.addStuffToImage(layout, 0)

        layer1 = layout.addLayer()
        self.addStuffToImage(layer1, 0)
        layer2 = layout.addLayer()
        layer3 = layout.addLayer()

        self.addStuffToImage(layer2, 1)
        self.addStuffToImage(layer3, 2)

        layout.draw()
        self.writeToFile(layout, "testgen-l.png")
        self.assertEqual((129, 94), layer1.size)
        self.assertEqual((129, 94), layer2.size)
        self.assertEqual((129, 94), layer3.size)

    def testTreeOfLayers(self):
        l1 = Layout((400, 200), 'h', border=5)
        self.addStuffToImage(l1)

        l2 = l1.addLayer(3)
        self.addStuffToImage(l2)

        l3 = l2.addLayer()
        self.addStuffToImage(l3)

        self.writeToFile(l1, "tree-l1.png")
        self.assertEqual(l1.size, (400, 200))
        self.assertEqual(l2.size, (390, 190))
        self.assertEqual(l3.size, (384, 184))

    def NewImage(self, layout):
        img = Image.new("P", layout.size, randint(0, 2))
        img.putpalette(Layout.DEFAULT_PALETTE)
        return img

    def NewDraw(self, img):
        return ImageDraw.Draw(img)

    def addStuffToImage(self, layout, childId=0):
        img = self.NewImage(layout)
        draw = self.NewDraw(img)

        draw.rectangle((5, 5) + tuple((dim - 5) for dim in layout.size), 1)
        text = "{id}\nchildId:{cid}\ndepth:{d}\ns:{size}".format(
            id=layout._id,
            cid=childId, d=layout._depth, size=layout.size)
        draw.text((10, 25), text)
        layout.setImage(img)
        layout.draw()


if __name__ == '__main__':
    unittest.main()
