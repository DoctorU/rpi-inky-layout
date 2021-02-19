import unittest
from .layout_fixtures import childlessLayout


class TestLayoutNoLayers(unittest.TestCase):

    def setUp(self):
        self.layout = childlessLayout()

    def testChildCount(self):
        self.assertEqual(0, self.layout._childCount())

    def testHasOneChild(self):
        self.assertFalse(self.layout._onlyOneChild())

    def testHasMoreThanOneChild(self):
        self.assertFalse(self.layout._moreThanOneChild())

    def testHasChildren(self):
        self.assertFalse(self.layout._hasChildren())
