from PIL import Image, ImageDraw
from random import randint
import numpy
from numpy import floor

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
        return "{id}/{depth}/{pm}/{pb}/{children}:{tl}+{dim}".format(
            id=self._id,
            depth=self._depth,
            tl=self.topLeft,
            dim=self.size,
            pb=self.packingBias,
            pm=self.packingMode,
            children=len(self.children)
        ) + "\nsl:{sl},b:{b},padd:{ps},sp:{sp},tl:{tl}".format(
                sl=self._slots,
                sp=self._spacers,
                b=self.borders,
                ps=self._padSpacers,
                tl=[c.topLeft for c in self.children]
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
        self.rotation_degrees = self.rotation.value * 90
        self.topLeft = (0, 0)
        self.packingMode = packingMode
        self.size = size
        if self.rotation.value % 2:
            self.size = self.tupleReversed(self.size)

        self.imageMode = imageMode

        print("Border", border)
        if isinstance(border, int):
            self.borders = (border, border, border, border)
            self.borderColour = 2
        elif isinstance(border, tuple):
            borders, self.borderColour = border
            if isinstance(borders, int):
                self.borders = (borders, borders, borders, borders)
            elif len(borders) == 2:
                btb, blr = borders
                self.borders = (btb, blr, btb, blr)
            elif len(borders) == 4:
                self.borders = borders
            else:
                raise("Illegal borders format: {b}".format(b=borders))

        elif not isinstance(border, None):
            raise("borders is not an allowed type:{t}".format(t=type(border)))

        self.children = []
        self._spacers = []
        self._padSpacers = []
        self._slots = []

        self._image = None
        self._depth = depth
        self._id = randint(1024, 8192)

    def transformAsNeeded(self, twod):
        if self.packingMode == 'v':
            twod = self.tupleReversed(twod)
        return twod

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

        self.children.append(childLayer)
        self._resizeChildren()
        return childLayer

    def resize(self, size):
        print ("--")
        self.size = size
        if self._image:
            self._image = self._image.crop((0, 0) + size)
        self._resizeChildren()
        print ("resized", self)

    def _childCount(self):
        return len(self.children)

    def _hasChildren(self):
        return self._childCount() > 0

    def _onlyOneChild(self):
        return self._childCount() == 1

    def _moreThanOneChild(self):
        return self._childCount() > 1

    def _calcDrawableSize(self):
        w, h = self.size
        bt, br, bb, bl = self.borders
        _calcDrawableSize = (w - bl - br, h - bt - bb)
        return _calcDrawableSize

    def _calcSlotSize(self):
        dw, dw1 = self.transformAsNeeded(self._calcDrawableSize())
        sw = self._sumSpacersWidth()
        w = dw - sw
        if self._onlyOneChild():
            return (w, dw1)
        w = w * 1.0
        slotCount = self._getChildSlotTotal()
        if slotCount > 1:
            w = w / slotCount
        return (int(floor(w)), dw1)

    def _getSlotSizeFor(self, child):
        slotSize = self._calcSlotSize()
        if self._moreThanOneChild():
            slotSize = (slotSize[0] * child.packingBias, slotSize[1])
        return self.transformAsNeeded(slotSize)

    def _calcSpacerErrorMargin(self):
        """The additional width to put into each spacer, to even things out."""
        drawableWidth, dh = self.transformAsNeeded(self._calcDrawableSize())
        _errorWidth = 0
        if self._hasChildren():
            _errorWidth = drawableWidth % self._childCount()

        return _errorWidth

    def _calcOptimumSpacerWidth(self):
        bt, br, bb, bl = self.borders
        if self.packingMode == 'h':
            return bl
        else:  # self.packingMode == 'v'
            return bt

    def _calcRealSpacerWidth(self, index):
        _optWidth = self._calcOptimumSpacerWidth()
        _padding = self._padSpacers[index]
        return _optWidth + _padding

    def _calcPadding(self, index):
        _padding = 0
        _totalError = self._calcSpacerErrorMargin()
        if index <= _totalError:
            _padding = _totalError
        return _padding

    def _calcTopLeft(self, index):
        slotSize = self._calcSlotSize()
        slotStart = self._getChildSlotStart(index)
        slotDeltas = ([dim * slotStart for dim in slotSize])
        topLeftBorders = (self.borders[0], self.borders[3])
        spacer = 0  # 0 offset from drawable area, NOT parent area
        if (index > 0):
            spacer = sum(self._spacers[0:index])
        if self.packingMode == 'h':
            left = spacer + slotDeltas[0]
            top = 0
        elif self.packingMode == 'v':
            left = 0
            top = spacer + slotDeltas[1]
        topLeft = (left + topLeftBorders[0], top + topLeftBorders[1])
        # FIXME
        breakpoint()
        return self.transformAsNeeded(topLeft)

    def _sumSpacersWidth(self):
        """The total width of all the spacers."""
        return sum(self._spacers)

    def _getSpacerWidthFor(self, index):
        return self._spacers[index]

    def _showSparePixels(self):
        if self.packingMode == 'h':
            borderIndex = 1
        else:
            borderIndex = 0
        size = self.transformAsNeeded(self.size)
        size0 = size[0]
        sumSpacers = sum(self._spacers)
        slotDims = [self.transformAsNeeded(slot)[0] for slot in self._slots]
        sumSlots = sum(slotDims)

        border1 = self.borders[1 - borderIndex]
        border2 = self.borders[3 - borderIndex]
        _sparePixels = (
            size0 - sumSpacers -
            sumSlots -
            border1 - border2
        )
        print("spare pixels:", _sparePixels, self)
        return _sparePixels

    def _resizeChildren(self):
        childCount = len(self.children)

        if childCount > 0:  # only update when there's children present

            # calc overall drawable size
            size = self._calcDrawableSize()

            # calc spacers
            spacerChildren = enumerate(self.children[1:])
            self._padSpacers = [
                self._calcPadding(i) for i, c in spacerChildren
            ]
            spacerChildren = enumerate(self.children[1:])
            # transformed viz packingMode
            self._spacers = [
                    self._calcRealSpacerWidth(i) for i, c in
                    spacerChildren
            ]

            self._slots = [
                self._getSlotSizeFor(child)
                for child
                in self.children
            ]
            # toplefts depend on slots
            self._topLefts = [
                self._calcTopLeft(i) for i, c in enumerate(self.children)
            ]

            self._showSparePixels()

            [
                self._resizeAChild(
                    child,
                    index
                ) for index, child in enumerate(self.children)
            ]
            print(self)

    def _resizeAChild(self, child, index):

        # slots come 'pre-transformed' for v/h
        slotSize = self._slots[index]
        topLeft = self._topLefts[index]
        bottomRight = tuple(zip(topLeft, slotSize))
        print("_resizeAChild", self.size, slotSize, topLeft, bottomRight)


        child.resize(slotSize)
        child.topLeft = topLeft

    def _getChildSlotTotal(self):
        """The total number of slots."""
        return self.getChildSlotCount(self.children)

    @staticmethod
    def getChildSlotCount(childrenList):
        """The count of the slot."""
        packingBias = [child.packingBias for child in childrenList]
        packingCount = sum(packingBias)
        return packingCount

    def _getChildSlotStart(self, index):
        """Which slot this child starts in."""
        return self.getChildSlotCount(self.children[0:index])

    def draw(self):
        if not self._image:
            self._image = Image.new(self.imageMode, self.size, self._depth)
        self._drawChildren()

        # draw the border
        draw = ImageDraw.Draw(self._image)
        if self.borders:
            self._drawBorder(draw)

        # return image rotated to the correct orientation
        return self._image.rotate(-self.rotation_degrees, expand=1)

    def _drawBorder(self, draw):
        w = self.borders[0]
        c = self.borderColour
        rectSize = tuple(numpy.subtract(self.size, 1))
        draw.rectangle([(0, 0), rectSize], outline=c, width=w)
        if len(self._spacers) > 0:
            print("TODO: DRAWING SPACERS")

    def _drawChildren(self):
        [child._drawChildren() for child in self.children]
        [
            self._drawChildOnParent(child, index)
            for index, child
            in enumerate(self.children)
        ]

    def _drawChildOnParent(self, child, index):
        if not child._image:
            print("WARNING: NO IMAGE SET ON THIS CHILD", child)
        else:
            if not self._image:
                self._image = self.setImage(child._image.copy())
            else:
                self._image.paste(child._image, child.topLeft)

    def write(self, fp):
        self.draw().convert(mode="RGB").save(fp)
        if self.children:
            [
                child.write(fp.replace(".", "-{i}.".format(i=index)))
                for index, child in enumerate(self.children)
            ]
