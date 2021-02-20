from PIL import Image, ImageDraw
from random import randint
import unittest
from . import layout_fixtures as fixtures

from rpi_inky_layout import Layout


class TestLayoutBasics(unittest.TestCase):

    @staticmethod
    def drawAndWrite(layout, filename):
        layout.write('test/expected-images/' + filename)

    def testCreateLonelyLayout(self):
        layout = fixtures.childlessLayout()
        self.assertEqual((200, 100), layout.size)

        img = self.NewImage(layout)
        draw = ImageDraw.Draw(img)
        draw.text((2, 50), 'testCreateLayout')
        layout.setImage(img)
        self.drawAndWrite(layout, 'testCreateLayout.png')

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
        self.drawAndWrite(layer1, 'Add2ChildrenHorizontalPacking1.png')

        layer2 = layout.addLayer()
        img = self.NewImage(layer2)
        draw = self.NewDraw(img)
        draw.text((2, 50), "layer 1-2", 2)
        layer2.setImage(img)

        self.assertEqual((97, 96), layer1.size)
        self.assertEqual((97, 96), layer2.size)
        self.drawAndWrite(layer2, 'Add2ChildrenHorizontalPacking2.png')
        self.drawAndWrite(layout, 'Add2ChildrenHorizontalPacking.png')

    def testAddChildrenPackedHWithBorderEnabledOneLayer(self):
        layout = fixtures.layoutWithLayers((600, 100), 1, border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((598, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledTwoLayers(self):
        layout = fixtures.twoLayers((600, 100), border=1)
        self.assertEqual(2, len(layout.children))
        [self.assertEqual(1, border) for border in layout.borders]
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((298, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledThreeLayers(self):
        layout = fixtures.threeLayers((600, 100), border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((198, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledFourLayers(self):
        layout = fixtures.fourLayers((600, 100), border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((148, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledFiveLayers(self):
        layout = fixtures.fiveLayers((600, 100), border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((118, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledSixLayers(self):
        layout = fixtures.layoutWithLayers((600, 100), 6, border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((98, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledSevenLayers(self):
        layout = fixtures.layoutWithLayers((600, 100), 7, border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((84, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledEightLayers(self):
        layout = fixtures.layoutWithLayers((600, 100), 8, border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        _7LayerWidth = 73
        [
            self.assertEqual((_7LayerWidth, 98), child.size)
            for child
            in layout.children
        ]
        layoutSpacerSum = sum(layout._spacers)
        self.assertEqual(12, layoutSpacerSum)
        layoutSlotSum = sum([x for x, y in layout._slots])
        self.assertEqual(_7LayerWidth * 8, layoutSlotSum)
        layoutBorderSum = layout.borders[1] + layout.borders[3]  # 2`
        self.assertEqual(2, layoutBorderSum)
        expectedWidth = layoutSpacerSum + layoutSlotSum + layoutBorderSum
        # FIXME BROKEN!!
        self.assertEqual(expectedWidth + 2, layout.size[0])
        self.drawAndWrite(
                layout, "testChildrenPackedHWithBorderEnabledEightLayers.png")

    # REVISIT
    def testGenerating2Layers(self):
        layout = fixtures.threeLayers((400, 100), border=3)
        layout.imageMode = "RGB"
        self.addStuffToImage(layout, 0, self.RandomColour())
        [
            self.addStuffToImage(child, i, self.RandomColour())
            for i, child
            in enumerate(layout.children)
        ]

        layout.draw()
        layout._showSparePixels()

        self.drawAndWrite(layout, "testGenerating2Layers.png")
        slotsW = sum([slot[0] for slot in layout._slots])
        borderW = layout.borders[1] + layout.borders[3]
        spacersW = sum(layout._spacers)
        padding = sum(layout._paddings)

        self.assertEqual(6, borderW)
        self.assertEqual(7, spacersW)
        # FIXME - 2 spare things - should be 4
        self.assertEqual(1, padding)
        # FIXME - 2 spare things - should be 0
        self.assertEqual(0, layout.size[0] - slotsW - borderW - spacersW)
        [
            self.assertEqual((129, 94), child.size)
            for child
            in layout.children
        ]

    def testTreeOfLayers(self):
        l1 = fixtures.childlessLayout((400, 200), border=5)
        l2 = l1.addLayer(3)
        l3 = l2.addLayer()

        self.addStuffToImage(l1)
        self.addStuffToImage(l2)
        self.addStuffToImage(l3)

        self.drawAndWrite(l1, "testTreeOfLayers.png")
        self.assertEqual(l1.size, (400, 200))
        self.assertEqual(l2.size, (390, 190))
        self.assertEqual(l3.size, (384, 184))

    def test_calcDrawableSize(self):
        layout = fixtures.childlessLayout((400, 200), border=0)
        self.assertEqual((400, 200), layout._calcDrawableSize())

        layout = fixtures.childlessLayout((400, 200), border=1)
        self.assertEqual((398, 198), layout._calcDrawableSize())

        layout = fixtures.childlessLayout((400, 200), border=((1, 2), 1))
        self.assertEqual((396, 198), layout._calcDrawableSize())

        layout = fixtures.childlessLayout((400, 200), border=((1, 2, 3, 4), 1))
        self.assertEqual((394, 196), layout._calcDrawableSize())

    def test_calcSpacerErrorMarginBorder5OneChild(self):
        layout = fixtures.oneLayer((400, 200), border=5)
        self.assertEqual((400 - 10) % 1, layout._calcSpacerErrorMargin(1))

    def test_calcSpacerErrorMarginBorder5TwoChildren(self):
        layout = fixtures.twoLayers((400, 200), border=5)
        self.assertEqual((400 - 10) % 2, layout._calcSpacerErrorMargin(1))

    def test_calcSpacerErrorMarginBorder5ThreeChildren(self):
        layout = fixtures.threeLayers((400, 200), border=5)
        self.assertEqual((400 - 10) % 3, layout._calcSpacerErrorMargin(1))

    def test_calcSpacerErrorMarginBorder3(self):
        layout = Layout((40, 200), border=3)
        layout.addLayer()
        print((40 - 6) % 1)
        self.assertEqual(0, layout._calcSpacerErrorMargin(1))
        layout.addLayer()
        print((40 - 6), (40 - 6) % 2)
        self.assertEqual(0, layout._calcSpacerErrorMargin(1))
        layout.addLayer()
        print((40 - 6), (40 - 6) % 3)
        self.assertEqual((40 - 6) % 3, layout._calcSpacerErrorMargin(0))

    def test_spacersWidth(self):
        layout = Layout((400, 200), border=1)
        layout.addLayer()
        layout.addLayer()
        self.assertEqual(1, layout._sumSpacersWidth())
        layout.addLayer()
        self.assertEqual(3, layout._sumSpacersWidth())

    def test_calcSlotWidthBorder5(self):
        layout = Layout((400, 200), border=5)

        # No Layers added yet
        self.assertEqual((390, 190), layout._calcSlotSize())
        layout.addLayer()
        self.assertEqual((390, 190), layout._calcSlotSize())
        layout.addLayer()
        self.assertEqual((192, 190), layout._calcSlotSize())

    def test_calcSlotWidthBorder4(self):
        layout = Layout((400, 200), border=4)
        layout.addLayer()
        self.assertEqual((392, 192), layout._calcSlotSize())
        layout.addLayer()
        self.assertEqual((194, 192), layout._calcSlotSize())

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


if __name__ == '__main__':
    unittest.main()
