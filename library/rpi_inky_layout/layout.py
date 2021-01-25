from PIL import Image, ImageDraw
from random import randint
import numpy

from .rotation import Rotation


"""
    Layout - a simple image layout manager for RPi Inky HATs.
"""


class Layout:

    DEFAULT_PALETTE = (255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252

    @staticmethod
    def tupleReversed(tupleValue):
        return tuple(reversed(tupleValue))

    def __str__(self):
        return "{id}/{depth}/{pb}/{children}:{tl}-{mid}-{dim}".format(
            id=self._id,
            depth=self._depth,
            tl=self.topleft,
            mid=self._middle,
            dim=self.size,
            pb=self.packingBias,
            children=len(self._children)
        )

    def __init__(
        self, size=(250, 122), packingMode='h', border=(0, 0),
        depth=0, rotation=Rotation.UP, packingBias=1, imageMode="RGB"
    ):
        """
            Construct a new Layer.

            Parameters
            ----------
            size: tuple
                A 2-tuple describing the size of the layer.
                Default:(250,122), the size of an Inky-PHAT.
            packingMode: str
                The packing mode: one of 'h' or 'v'.
            border: int|(0,0)
                If an int, then the width, and the colour is assumed to be '2'.
                If a 2-tuple, then the first part is the width, and the second
                is the colour.
            depth: int
                for tracking the tree hierarchy - for internal use
                only. Default:0.
            rotation: Rotation
                The type of rotation. This modifies the way that
                images are drawn, so that UP becomes the default top, DOWN
                would render upside down, and left and right similarly modify
                the rendering.
            packingBias: int
                The packing bias. If you add 2 layers: one with
                default bias, one with packingBias=3, then the second layer
                will take up 3/4 of the width (3+1 = 4 = 100%).
            imageMode: str
                The image mode to use when creating a default image (when one
                does not exist). Refer to
                [Pillow image modes](https://pillow.readthedocs.io/en/latest/handbook/concepts.html#modes).
        """  # noqa: E501
        self.rotation = rotation
        self.packingBias = packingBias
        if self.rotation.value % 2:
            self.size = self.tupleReversed(size)
        else:
            self.size = size
        self.rotation_degrees = self.rotation.value * 90
        self._middle = tuple(dim / 2 for dim in size)
        self.topleft = (0, 0)
        self.packingMode = packingMode
        self.imageMode = imageMode

        if isinstance(border, int):
            self.borderWidth = border
            self.borderColour = 2
        elif isinstance(border, tuple):
            self.borderWidth, self.borderColour = border
        elif not isinstance(border, None):
            raise("border is not an allowed type:{t}".format(t=type(border)))

        self._children = []
        self._image = None
        self._depth = depth
        self._id = randint(1024, 8192)

    def setImage(self, image):
        """
            Set the image on this layer after you've drawn it.
            The image you set will be cropped to the Layer's size before being
            set on it.
        """
        self._image = image.crop((0, 0) + self.size)
        return self._image

    def addLayer(
            self,
            border=0,
            packingBias=1,
            packingMode='h',
            rotation=Rotation.UP
    ):
        """
            Add a new child layout to this layout as a layer.

            Parameters
            ------
            border: int | (int, colour)
                the same as the constructor's border property.
            packingBias: int
                the same as the constructor's packingBias property.
        """

        childLayer = Layout(
            depth=self._depth + 1,
            border=border,
            packingBias=packingBias,
            packingMode=packingMode,
            rotation=rotation
            )

        self._children.append(childLayer)
        self._resizeChildren()
        return childLayer

    def addLayerFrom(self, proto):
        self.addLayer(
            border=proto.border,
            packingBias=proto.packingBias,
            packingMode=proto.packingMode,
            rotation=proto.rotation
        )

    def resize(self, size, border=(0, 0)):
        size = numpy.subtract(size, border)
        size = tuple(round(dim) for dim in size)
        self.size = size
        if self._image:
            self._image = self._image.crop((0, 0) + size)
        self._resizeChildren()

    def _resizeChildren(self):

        childCount = len(self._children)

        if childCount > 0:  # only update when there's children present

            size = self.size
            if self.packingMode == 'v':
                size = self.tupleReversed(size)

            # Calculating values for each Child:
            packingCount = self._getChildrenPackingBiasTotal()

            slotMid = (size[0] / packingCount, size[1])
            slotMid = tuple(dim / 2 for dim in slotMid)

            # slotSize is the size of each slot.
            # multiple slotSize by layout's packingBias to get its true size
            slotSize = tuple(dim * 2 for dim in slotMid)

            # border doesn't change with packingBias
            borderWidth = self.borderWidth
            border0 = borderWidth * (childCount + 1) / childCount
            border1 = borderWidth * 2
            border = (border0, border1)

            if self.packingMode == 'v':
                slotSize = self.tupleReversed(slotSize)
                border = self.tupleReversed(border)

            [
                self._resizeAChild(
                    child,
                    index,
                    slotSize,
                    slotMid,
                    border,
                    packingCount
                ) for index, child in enumerate(self._children)
            ]

    def _resizeAChild(
            self,
            child, index, slotSize, slotMid, border, packingCount):

        childStartSlot = self._getChildPackingBiasStart(index)

        if(self.packingMode == 'v'):
            slotSize = self.tupleReversed(slotSize)

        # calculate the new size
        slotSize0, slotSize1 = slotSize
        # calculate the new top-left FIRST (depends on final slot position)
        borderOffset = self.borderWidth * (index + 1)
        tlOffset0 = slotSize0 * childStartSlot
        topleft = (int(borderOffset + tlOffset0),  int(self.borderWidth))

        # Calculate the new slot size 0-dimension
        size0 = slotSize0 * child.packingBias
        size = (size0, slotSize1)

        childMid = (slotMid[0] * child.packingBias, slotMid[1])

        if(self.packingMode == 'v'):
            size = self.tupleReversed(size)
            childMid = self.tupleReversed(childMid)
            topleft = self.tupleReversed(topleft)

        child.resize(size, border)
        # This is broken
        child.middle = childMid
        child.topleft = topleft

    def draw(self):
        if not self._image:
            self._image = Image.new(self.imageMode, self.size, self._depth)
        self._drawChildren()

        # draw the border
        draw = ImageDraw.Draw(self._image)
        if self.borderWidth:
            self._drawBorder(draw)

        # return image rotated to the correct orientation
        return self._image.rotate(-self.rotation_degrees, expand=1)

    def _drawBorder(self, draw):
        w = self.borderWidth
        c = self.borderColour
        draw.rectangle([(0, 0), self.size], outline=c, width=w)
        count = len(self._children)
        for i, child in enumerate(self._children):
            if(self.packingMode == 'h'):
                xy = [
                    (self.size[0] / count * (i + 1), 0),
                    (self.size[0] / count * (i + 1), self.size[1])
                ]
                draw.line(xy, c, w)
            if(self.packingMode == 'v'):
                xy = [
                    (0, self.size[1] / count * (i + 1)),
                    (self.size[0], self.size[1] / count * (i + 1))
                ]
                draw.line(xy, c, w)

    def _getChildrenPackingBiasTotal(self):
        return self.getChildrenPackingBiasCount(self._children)

    @staticmethod
    def getChildrenPackingBiasCount(childrenList):
        packingBias = [child.packingBias for child in childrenList]
        packingCount = sum(packingBias)
        return packingCount

    def _getChildPackingBiasStart(self, index):
        return self.getChildrenPackingBiasCount(self._children[0:index])

    def _drawChildren(self):
        [child._drawChildren() for child in self._children]
        [
            self._drawChildOnParent(child, index)
            for index, child
            in enumerate(self._children)
        ]

    def _drawChildOnParent(self, child, index):
        if not child._image:
            print("WARNING: NO IMAGE SET ON THIS CHILD", child)
        else:
            if not self._image:
                self._image = self.setImage(child._image.copy())
            else:
                self._image.paste(child._image, child.topleft)

    def write(self, fp):
        self.draw().convert(mode="RGB").save(fp)
        if self._children:
            [
                child.write(fp.replace(".", "-{i}.".format(i=index)))
                for index, child in enumerate(self._children)
            ]
