#!/usr/bin/env python3
from math import floor
from Layout import Layout
from random import randint
import unittest
from PIL import Image, ImageDraw

class TestLayout(unittest.TestCase):

    def writeToFile(self, layout, filename):
        layout.write( filename )

    def testCreateLayout(self):
        l = Layout( (200,100) )
        self.assertEqual( (200,100), l.size )

        filename = 'testCreateLayout1.png'
        # Create the img
        img = self.NewImage(l)
        # draw on it
        draw = ImageDraw.Draw(img)
        draw.text( (2,50), filename)
        #set it on the layer
        l.setImage(img)
        # render it
        l.draw()
        #Write it
        l.write(filename)

    def testAdd2ChildrenHorizontalPacking(self):
        l = Layout( (200,100), 'h', border=2)
        img = self.NewImage(l)
        draw = self.NewDraw(img)
        draw.text( (2,50), "main layout 1", 2)
        l.setImage(img)
        layer1 = l.addLayer( )

        img = self.NewImage(layer1)
        draw = self.NewDraw(img)
        draw.text( (2,50), "layer 1-1", 2)
        layer1.setImage(img)

        self.assertEqual( (196, 96), layer1.size )
        layer1.write( 'test2.png')

        layer2 = l.addLayer()
        img = self.NewImage(layer2)
        draw = self.NewDraw(img)
        draw.text( (2,50), "layer 1-2", 2)
        layer2.setImage(img)

        self.assertEqual( (97, 96), layer1.size )
        self.assertEqual( (97, 96), layer2.size )
        layer2.write( 'test3.png')

    def testAdd2ChildrenVerticalPacking(self):
        l = Layout( (200,100), 'v')

        layer1 = l.addLayer( )
        self.assertEqual( (200,100), layer1.size )

        layer2 = l.addLayer()
        self.assertEqual( (200,50), layer1.size )
        self.assertEqual( (200,50), layer2.size )

    def testAddChildrenPackedVWithBorderEnabled(self):
        l = Layout( (200,300), 'v', 1 )
        layer1 = l.addLayer( )
        self.assertEqual( (198,298), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (198,148 ), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (198,99 ), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (198,74), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (198,59), layer1.size )



    def testAddChildrenPackedHWithBorderEnabled(self):
        l = Layout( (200,300), 'h', 1 )
        layer1 = l.addLayer( )
        self.assertEqual( (198,298), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (98, 298), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (65, 298), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (49, 298), layer1.size )

        layer1 = l.addLayer( )
        self.assertEqual( (39, 298), layer1.size )

        layer1 = l.addLayer()
        self.assertEqual( (32, 298), layer1.size )

        layer1 = l.addLayer()
        self.assertEqual( (27, 298), layer1.size )

        layer1 = l.addLayer()
        self.assertEqual( (24, 298), layer1.size )


    def testTestGenerating2Layers(self):
        l = Layout( (400,100), 'h', border=3)
        #self.addStuffToImage(l)
        self.addStuffToImage(l, 0)

        layer1 = l.addLayer()
        self.addStuffToImage(layer1, 0)
        layer2 = l.addLayer()
        layer3 = l.addLayer()

        self.addStuffToImage(layer2, 1)
        self.addStuffToImage(layer3, 2)

        print (l, layer1, layer2, layer3)

        l.draw()
        l.write("testgen-l.png")
        layer1.write("testgen-l1.png")
        layer2.write("testgen-l2.png")
        layer3.write("testgen-l3.png")
        self.assertEqual( (129,94), layer1.size)
        self.assertEqual( (129,94), layer2.size)
        self.assertEqual( (129,94), layer3.size)
        print("/testTestGenerating2Layers")

    def testTreeOfLayers(self):
        l1 = Layout ( (400,200), 'h', border=5)
        self.addStuffToImage(l1)

        l2 = l1.addLayer(3)
        self.addStuffToImage(l2)

        l3 = l2.addLayer()
        self.addStuffToImage(l3)

        l1.draw()
        l1.write("tree-l1.png")
        l2.write("tree-l2.png")
        l3.write("tree-l3.png")
        self.assertEqual(l1.size, (400,200))
        self.assertEqual(l2.size, (390,190))
        self.assertEqual(l3.size, (384,184))

    def NewImage(self, layout):
        img = Image.new("P", layout.size, randint(0,2))
        img.putpalette(Layout.DEFAULT_PALETTE)
        return img

    def NewDraw(self, img):
        return ImageDraw.Draw(img)

    def addStuffToImage(self, layout, childId=0):
        img = self.NewImage(layout)
        draw = self.NewDraw(img)

        diff = -5
        draw.rectangle((5,5) + tuple((dim - 5) for dim in layout.size) , 1)
        text = "{id}\nchildId:{cid}\ndepth:{d}\ns:{size}".format(
            id=layout._id,
            cid=childId, d=layout._depth,size=layout.size)
        draw.text((10,25), text)
        layout.setImage(img)
        layout.draw()

if __name__ == '__main__':
    unittest.main()
