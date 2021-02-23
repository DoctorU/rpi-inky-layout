import unittest
from PIL import Image, ImageDraw

from rpi_inky_layout import Layout


def newImage(_size, backgroundcol):
    img = Image.new("P", _size, backgroundcol)
    img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
    return img


class LayoutSub(Layout):

    def __init__(self):
        super().__init__((200, 200))

    def drawOverride(self):

        self._image = newImage(self.size, 0)
        draw = ImageDraw.Draw(self._image)

        def half_difference(x1, x2):
            return int((x1 - x2) / 2)

        text_x1, text_y1 = draw.textsize("LayoutSub")
        text_x2, text_y2 = self.size
        text_pos = (
            half_difference(text_x2, text_x1),
            half_difference(text_y2, text_y1)
        )
        draw.text(text_pos, "LayoutSub", fill=1)


class TestIssue43(unittest.TestCase):

    @staticmethod
    def writeImage(layout, filename):
        layout.write('test/expected-images/' + filename)

    def testChildrenDraw(self):
        layout = Layout((200, 200))
        child = LayoutSub()
        layout.addLayout(child)
        otherChild = layout.addLayer(packingMode='v')
        otherChild.addLayout(LayoutSub())
        otherChild.addLayout(LayoutSub())
        self.writeImage(layout, "testChildrenDraw.gif")

    def testChildrenSetImage(self):
        layout = Layout((200, 200))
        child = LayoutSub()
        otherChild = layout.addLayer(packingMode='v')
        otherChild.addLayout(LayoutSub())
        otherChild.addLayout(LayoutSub())
        layout.addLayout(child)
        img = child.draw()
        child.setImage(img)
        self.writeImage(layout, "testChildrenSetImage.gif")


if __name__ == '__main__':
    unittest.main()
