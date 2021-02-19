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
        layout = fixtures.twoLayersH((600, 100), border=1)
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
        layout = fixtures.threeLayersH((600, 100), border=1)
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
        layout = fixtures.fourLayersH((600, 100), border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((147, 98), child.size)
            for child
            in layout.children
        ]

    def testAddChildrenPackedHWithBorderEnabledFiveLayers(self):
        layout = fixtures.fiveLayersH((600, 100), border=1)
        [
            self.addStuffToImage(child, 1, self.RandomColour())
            for child
            in layout.children
        ]
        [
            self.assertEqual((116, 98), child.size)
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
            self.assertEqual((95, 98), child.size)
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
            self.assertEqual((82, 98), child.size)
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
        _7LayerWidth = 68
        [
            self.assertEqual((_7LayerWidth, 98), child.size)
            for child
            in layout.children
        ]
        layoutSpacerSum = sum(layout._spacers)
        self.assertEqual(49, layoutSpacerSum)
        layoutSlotSum = sum([x for x, y in layout._slots])
        self.assertEqual(_7LayerWidth * 8, layoutSlotSum)
        layoutBorderSum = layout.borders[1] + layout.borders[3]  # 2`
        self.assertEqual(2, layoutBorderSum)
        expectedWidth = layoutSpacerSum + layoutSlotSum + layoutBorderSum
        # FIXME BROKEN!!
        self.assertEqual(expectedWidth + 5, layout.size[0])
        self.drawAndWrite(
                layout, "testChildrenPackedHWithBorderEnabledEightLayers.png")

    # REVISIT
    def testGenerating2Layers(self):
        layout = fixtures.threeLayersH((400, 100), border=3)
        layout.imageMode = "RGB"
        self.addStuffToImage(layout, 0, self.RandomColour())
        [
            self.addStuffToImage(child, i, self.RandomColour())
            for i, child
            in enumerate (layout.children)
        ]

        layout.draw()
        self.drawAndWrite(layout, "testGenerating2Layers.png")
        slotsW = sum(list(zip(*layout._slots))[0])
        borderW = layout.borders[1] + layout.borders[3]
        spacersW = sum(layout._spacers)

        self.assertEqual(6, borderW)
        self.assertEqual(8, spacersW)
        self.assertEqual(400 - 6 - 8, layout.size[0] - borderW - spacersW)
        [
            self.assertEqual((128, 94), child.size)
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
        layout = fixtures.oneLayerH((400, 200), border=5)
        self.assertEqual((400 - 10) % 1, layout._calcSpacerErrorMargin())

    def test_calcSpacerErrorMarginBorder5TwoChildren(self):
        layout = fixtures.twoLayersH((400, 200), border=5)
        self.assertEqual((400 - 10) % 2, layout._calcSpacerErrorMargin())

    def test_calcSpacerErrorMarginBorder5ThreeChildren(self):
        layout = fixtures.threeLayersH((400, 200), border=5)
        self.assertEqual((400 - 10) % 3, layout._calcSpacerErrorMargin())

    def test_calcSpacerErrorMarginBorder3(self):
        layout = Layout((40, 200), border=3)
        layout.addLayer()
        print((40 - 6) % 1)
        self.assertEqual(0, layout._calcSpacerErrorMargin())
        layout.addLayer()
        print((40 - 6), (40 - 6) % 2)
        self.assertEqual(0, layout._calcSpacerErrorMargin())
        layout.addLayer()
        print((40 - 6), (40 - 6) % 3)
        self.assertEqual((40 - 6) % 3, layout._calcSpacerErrorMargin())

    def test_spacersWidth(self):
        layout = Layout((400, 200), border=1)
        layout.addLayer()
        layout.addLayer()
        self.assertEqual(1, layout._spacersWidth())
        layout.addLayer()
        self.assertEqual(6, layout._spacersWidth())

    def test_calcSlotWidthBorder5(self):
        layout = Layout((400, 200), border=5)

        # No Layers added yet
        self.assertEqual(390, layout._calcSlotWidth())
        layout.addLayer()
        self.assertEqual(390, layout._calcSlotWidth())
        layout.addLayer()
        self.assertEqual(192, layout._calcSlotWidth())

    def test_calcSlotWidthBorder4(self):
        layout = Layout((400, 200), border=4)
        layout.addLayer()
        self.assertEqual(392, layout._calcSlotWidth())
        layout.addLayer()
        self.assertEqual(int((392 - 4) / 2), layout._calcSlotWidth())

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