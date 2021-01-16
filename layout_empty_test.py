#!/usr/bin/env python3
from math import floor
from Layout import Layout
import unittest

class TestStringMethods(unittest.TestCase):

    def writeToFile(self, layout, filename):
        layout.write( filename )

    def testCreateLayout(self):
        l = Layout( (200,100) )
        self.assertEqual( (200,100), l.dimensions )
        filename = "test1.png"
        l.get_ImageDraw().text( (0,50), filename)
        self.writeToFile(l, filename)
        l.get_ImageDraw()

    def testAdd2ChildrenHorizontalPacking(self):
        l = Layout( (200,100), 'h')
        l.get_ImageDraw().text( (0,50), "main layout 1")
        layer1 = l.addLayer( )
        layer1.get_ImageDraw().text( (0,50), "layer 1-1")
        
        self.assertEqual( (200,100), layer1.dimensions )
        self.writeToFile(l, 'test2.png')
        with self.assertRaises(Exception):
            l.get_ImageDraw()

        layer2 = l.addLayer()
        layer2.get_ImageDraw().text( (0,50), "layer 1-2")
        self.assertEqual( (100,100), layer1.dimensions )
        self.assertEqual( (100,100), layer2.dimensions )
        self.writeToFile(l, 'test3.png')
        with self.assertRaises(Exception):
            l.get_ImageDraw()

    def testAdd2ChildrenVerticalPacking(self):
        l = Layout( (200,100), 'v')
        l.get_ImageDraw().text( (0,50), "main layout 2")
        layer1 = l.addLayer( )
        layer1.get_ImageDraw().text( (0,50), "layer 2-1")
        self.assertEqual( (200,100), layer1.dimensions )
        with self.assertRaises(Exception):
            l.get_ImageDraw()

        layer2 = l.addLayer()
        layer2.get_ImageDraw().text( (0,50), "layer 1-2")
        self.assertEqual( (200,50), layer1.dimensions )
        self.assertEqual( (200,50), layer2.dimensions )
        with self.assertRaises(Exception):
            l.get_ImageDraw()
            
    def testAddChildrenPackedVWithBorderEnabled(self):
        l = Layout( (200,300), 'v', 1 )
        layer1 = l.addLayer( )
        self.assertEqual( (198,298), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (198,147 ), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (198,96 ), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (198,70), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (198,54), layer1.dimensions )



    def testAddChildrenPackedHWithBorderEnabled(self):
        l = Layout( (200,300), 'h', 1 )
        layer1 = l.addLayer( )
        self.assertEqual( (198,298), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (97, 298), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (62, 298), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (45, 298), layer1.dimensions )

        layer1 = l.addLayer( )
        self.assertEqual( (34, 298), layer1.dimensions )


if __name__ == '__main__':
    unittest.main()
