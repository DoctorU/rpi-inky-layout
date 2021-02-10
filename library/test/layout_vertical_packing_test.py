from PIL import Image, ImageDraw
from random import randint
import unittest

from rpi_inky_layout import Layout


class TestLayoutVerticalBasics(unittest.TestCase):

    @staticmethod
    def drawAndWrite(layout, filename):
        layout.write('test/expected-images/' + filename)

    def testAdd2ChildrenVerticalPacking(self):
        layout = Layout((200, 100), 'v')

        layer1 = layout.addLayer()
        self.assertEqual((200, 100), layer1.size)

        layer2 = layout.addLayer()
        self.assertEqual((200, 50), layer1.size)
        self.assertEqual((200, 50), layer2.size)
        layer1.setImage(self.NewImage(layer1, "RGB"))
        self.addStuffToImage(layer1, 1, self.RandomColour())
        layer2.setImage(self.NewImage(layer2, "RGB"))
        self.addStuffToImage(layer2, 1, self.RandomColour())

        self.drawAndWrite(layout, 'testAdd2ChildrenVerticalPacking.png')

    # REVISIT
    def testAddChildrenPackedVWithBorderEnabled(self):
        layout = Layout((200, 300), 'v', border=1)
        layer1 = layout.addLayer()
        self.assertEqual((198, 298), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 149), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 99), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 74), layer1.size)

        layer1 = layout.addLayer()
        self.assertEqual((198, 60), layer1.size)

    def NewImage(self, layout, mode='P', colour=randint(0, 2)):
        img = Image.new(mode, layout.size, colour)
        if mode == 'P':
            img.putpalette(Layout.DEFAULT_PALETTE)
        return img

    def RandomColour(self):
        return (randint(64, 255), randint(64, 255), randint(64, 255))

    def NewDraw(self, img):
        return ImageDraw.Draw(img)

    def addStuffToImage(self, layout, childId=0, bgcolour=(128, 128, 1)):

        img = self.NewImage(layout, "RGB", bgcolour)
        draw = self.NewDraw(img)
        text = "{id}\nchildId:{cid}\ndepth:{d}\ns:{size}\ntl:{tl}".format(
            id=layout._id,
            cid=childId, d=layout._depth, size=layout.size, tl=layout.topLeft)
        tsize = draw.textsize(text)
        if(tsize[1] > layout.size[1]):
            text = "{id}/{cid} d:{d}\ns:{size} tl:{tl}".format(
                id=layout._id, cid=childId, d=layout._depth,
                size=layout.size, tl=layout.topLeft)
        # draw.rectangle((0, 0), 1)
        draw.text((5, 5), text)
        layout.setImage(img)
        layout.draw()

    def InterrogateLayer(self, layout):
        print("parent size: {ps}".format(ps=layout.size))
        print("parent:borders: {b}".format(b=layout.borders))
        print("parent:drawable-size: {s}".format(s=layout._drawableSize()))
        print("parent:slot-width: {s}".format(s=layout._slotWidth()))
        for i, child in enumerate(layout._children):

            print("child-{i}:top-left: {tl}".format(i=i, tl=child.topLeft))
            print("child-{i}:size: {s}".format(i=i, s=child.size))


if __name__ == '__main__':
    unittest.main()
