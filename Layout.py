from PIL import Image, ImageDraw, ImageChops
from math import floor
from random import randint
import numpy

class Layout:

    DEFAULT_PALETTE = (255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252

    def __init__(self, size=(250,122), packingMode='h', border=(0,0), depth=0):
        self.size = size
        self._dimensions = tuple(s*1.0 for s in size)
        self._middle = tuple(dim/2 for dim in size)
        self.topleft = (0,0)
        self.packingMode = packingMode
        print("type of border: ", type(border))
        if isinstance(border, int):
            self.borderWidth = border
            self.borderColour = 2
        elif isinstance(border, tuple):
            self.borderWidth = border[0]
            self.borderColour = border[1]
        elif not isinstance(border, None):
            raises ("border is not an allowed type:{t}".format(t=type(border)))
        self._children = []
        self._image = None
        self._depth=depth
        self._id = randint(1024,8192)

    def setImage(self, image):
        self._image = image.crop((0,0)+self.size)

    def getDimensions(self):
        return self.size;

    def addLayer(self, border=1):
        #add a child Layer to the child list, then resize them all
        childLayer = Layout(depth=self._depth + 1, border=border) # make it at least the same size
        self._children.append(childLayer)
        self._updateChildren()
        return childLayer

    def resize(self, size):
        print(self, "resizing to ", size)
        self.size = size
        if self._image:
            self._image = self._image.crop((0,0) + size)
        self._updateChildren()

    def reposition(self, size, topleft=(0,0)):
        self.topleft = topleft
        self.resize(size)

    def __str__(self):
        return "{id}/{depth}:{tl}:{dim}:{mid}:{children}".format(
            id = self._id,
            depth = self._depth,
            tl = self.topleft,
            mid = self._middle,
            dim = self.size,
            children = len(self._children)
        )

    """
        _updateChildren

        Iterates over all children of this Layout, and resizes them, and sets their positions
    """
    def _updateChildren(self):
        childCount = len(self._children)
        if childCount > 0: # only update when there's children present
            size = self.size
            borderWidth = self.borderWidth
            if self.packingMode == 'v':
                size = tuple(reversed(size))
#
            childMid = (size[0]/childCount, size[1])
            childMid = tuple(dim/2 for dim in childMid)
            size = (((childMid[0]*2)-(borderWidth*(childCount+1))), ((childMid[1]-borderWidth)*2))
            size = tuple(round(dim) for dim in size)

            if self.packingMode == 'v':
                size = tuple(reversed(size))

            print (" self - size:", self.size,
                " border:",borderWidth,
                " packing:", self.packingMode,
                "child - count:", childCount,
                " size:", size)

            print("gonna resize", childCount, self.packingMode,
            "\n border:", borderWidth,
            " child new dimension: ", size)
            [child.resize(size) for child in self._children]
            [child._setMiddle(childMid) for child in self._children]

    def _setMiddle(self, middle):
        self._middle = middle

    def draw(self):
        if not self._image:
            self._image = Image.new("P", self.size, self._depth)
        self._drawChildren()
        # draw the border
        draw = ImageDraw.Draw(self._image)
        if self.borderWidth:
            self._drawBorder(draw)

    def _drawBorder(self, draw):
        w = self.borderWidth
        c = self.borderColour
        draw.rectangle([(0,0),self.size], outline=c, width=w)
        count = len(self._children)
        for i,child in enumerate(self._children):
            if(self.packingMode == 'h'):
                xy = [(self.size[0]/count*(i+1), 0), (self.size[0]/count*(i+1),self.size[1]) ]
                draw.line(xy, c, w)
            if(self.packingMode == 'v'):
                xy = [ (0, self.size[1]/count*(i+1)), (self.size[0],self.size[1]/count*(i+1)) ]
                draw.line(xy, c, w)

    def _drawChildren(self):
        [child._drawChildren() for child in self._children]
        [self._drawChildOnParent(child,index) for index,child in enumerate(self._children)]

    def _drawChildOnParent(self, child, index):
        print("_drawChildOnParent", self, child, index)
        # child contains the image to paste; index helps calculate the offset
        size = child.size
        tl = child.topleft
        print("child:{c}".format(c=child))
        if self.packingMode == 'h':
            size = tuple(reversed(size))
        # SOMETHING IS WRONG HERE!
        childPos = ( self.borderWidth, self.borderWidth * (index+1) + (size[1] * index))
        if self.packingMode == 'h':
            childPos = tuple(reversed(childPos))
        print ("index:{i}, size:{s}, pos:{pos}".format(i=index, s=size, pos=childPos))

        if not child._image:
            print ("WARNING: NO IMAGE SET ON THIS CHILD", child);
        else:
            print("Child position: ", childPos, child.size, child._image.size,
                "\non parent: ", self.size,
                "\ndiff:image.size self-child:", numpy.subtract(self._image.size, child._image.size),
                "diff:size self-child:", numpy.subtract(self.size, child.size))
            self._image.paste(child._image, childPos)
            #self._image.paste(child._image, (200,0))

    def write(self, fp):
        self.draw()
        self._image.save(fp)
        if self._children:
            [ child.write(str(index) +"-"+ fp) for index, child in enumerate(self._children)]

    def report(self, message):
        print(message)
