from enum import Enum, unique
from PIL import Image, ImageDraw
from math import floor
from random import randint
import numpy

@unique
class Rotation(Enum):
    UP=0 # Normal
    RIGHT=1 # rotate left 90°
    DOWN=2 # rotate 180°
    LEFT=3 # rotate right 90°

class Layout:
    """
        Layout - a simple image layout manager for RPi Inky HATs.
    """

    DEFAULT_PALETTE = (255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252

    def __init__(self, size=(250,122), packingMode='h', border=(0,0), depth=0, rotation=Rotation.UP):
        """
            Construct a new Layer.
            :param:size: the size of the layer. default:(250,122) (the size of an Inky-pHAT).
            :param:packingMode: the packing mode, one of 'h' or 'v'.
            :param:border: a border definition.
                If an int, then the width, and the colour is assumed to be '2'.
                If a 2-tuple, then the first part is the width, and the second is the colour.
            :param:depth: for tracking the tree hierarchy - for internal use only. Default:0.
            :param:rotation: the type of rotation. This modifies the way that images are drawn, so that
                UP becomes the default top, DOWN would render upside down, and left and right similarly modify
                the rendering.

        """
        self.rotation = rotation
        print (self.rotation, self.rotation.value, self.rotation.value %2)
        if self.rotation.value % 2:
            self.size = tuple(reversed(size)) # 1,3
        else:
            self.size = size
        self.rotation_degrees = self.rotation.value * 90
        #self._dimensions = tuple(s*1.0 for s in size)
        self._middle = tuple(dim/2 for dim in size)
        self.topleft = (0,0)
        self.packingMode = packingMode

        if isinstance(border, int):
            self.borderWidth = border
            self.borderColour = 2
        elif isinstance(border, tuple):
            self.borderWidth, self.borderColour = border
        elif not isinstance(border, None):
            raises ("border is not an allowed type:{t}".format(t=type(border)))

        self._children = []
        self._image = None
        self._depth = depth
        self._id = randint(1024,8192)

    def setImage(self, image):
        """
            setImage
            Set the image on this layer after you've drawn it.
            The image you set will be cropped to the Layer's size before being set on it.
        """
        self._image = image.crop((0,0)+self.size)

    def addLayer(self, border=1):
        """
            addLayer(border=1)
            Add a new layer to this Layer.
            :param:border: the same as the constructor's border property.
        """
        #add a child Layer to the child list, then resize them all
        childLayer = Layout(depth=self._depth + 1, border=border) # make it at least the same size
        self._children.append(childLayer)
        self._updateChildren()
        return childLayer

    def resize(self, size):
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

            border0 = borderWidth*(childCount + 1)/childCount
            border1 = borderWidth*2
            size0 = childMid[0]*2
            size1 = childMid[1]*2

            size = (size0 - border0, size1 - border1)
            size = tuple(round(dim) for dim in size)

            if self.packingMode == 'v':
                size = tuple(reversed(size))

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
        return self._image.rotate(-self.rotation_degrees, expand=1)

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

        # child contains the image to paste; index helps calculate the offset
        size = child.size
        tl = child.topleft

        if self.packingMode == 'v':
            size = tuple(reversed(size))

        borderOffset = self.borderWidth*(index+1)
        tlOffset0 = size[0]*index
        childPos = (borderOffset + tlOffset0,  self.borderWidth)
        if self.packingMode == 'v':
            childPos = tuple(reversed(childPos))

        if not child._image:
            print ("WARNING: NO IMAGE SET ON THIS CHILD", child);
        else:
            self._image.paste(child._image, childPos)

    def write(self, fp):
        self.draw().save(fp)
        if self._children:
            [ child.write(fp.replace(".", "-{i}.".format(i=index))) for index, child in enumerate(self._children)]
