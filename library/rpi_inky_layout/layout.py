from PIL import Image, ImageDraw
from random import randint
import numpy
from numpy import floor

from .rotation import Rotation


class Layout:
    """
        Layout - a simple image layout manager for RPi Inky HATs.
    """

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
            children=self._childCount()
        ) + "\nsl:{sl},b:{b},padd:{ps},sp:{sp},tl:{tl}".format(
                sl=self._slots,
                sp=self._spacers,
                b=self.borders,
                ps=self._paddings,
                tl=self._topLefts
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
        self.drawBorders = True
        self.packingMode = packingMode
        self.size = size
        if self.rotation.value % 2:
            self.size = self.tupleReversed(self.size)

        self.imageMode = imageMode

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
        self._paddings = []
        self._topLefts = []
        self._slots = []
        self._error = 0.0
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
        self._error = 0.0
        self.children.append(childLayer)
        self._resizeChildren()
        return childLayer

    def resize(self, size):
        self.size = size
        if self._image:
            self._image = self._image.crop((0, 0) + size)
        self._resizeChildren()

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
        # Remove the borders
        w = w - bl - br
        h = h - bt - bb
        if self.packingMode == 'h':
            # Adjust the width to be a round number...
            h = h
        _calcDrawableSize = (w, h)
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
        intW = int(floor(w))  # FIXME this underuses the drawable size
        self._error = self._error + w - intW
        return (intW, dw1)

    def _getSlotSizeFor(self, child):
        slotSize = self._calcSlotSize()
        if self._moreThanOneChild():
            slotSize = (slotSize[0] * child.packingBias, slotSize[1])
        return self.transformAsNeeded(slotSize)

    def _calcSpacerErrorMargin(self, index):
        """The additional width to put into each spacer, to even things out."""
        drawableWidth, dh = self.transformAsNeeded(self._calcDrawableSize())
        _errorWidth = 0
        if self._hasChildren():
            childCount = self._childCount()
            _errorWidth = (drawableWidth % childCount)
            if _errorWidth > 0:
                _perChildW = _errorWidth / childCount
                _diff = 1
                if index > 0:
                    _this = floor(_perChildW * index)
                    _prev = floor(_perChildW * (index - 1))
                    _diff = _this - _prev
                _errorWidth = int(_diff)
        return _errorWidth

    def _calcPadding(self, index):
        _padding = 0
        _paddingError = self._calcSpacerErrorMargin(index)
        # if index <= _totalError:
        _padding = _paddingError
        return _padding

    def _calcOptimumSpacerWidth(self):
        bt, br, bb, bl = self.borders
        if self.packingMode == 'h':
            return bl
        else:  # self.packingMode == 'v'
            return bt

    def _calcRealSpacerWidth(self, index):
        _optWidth = self._calcOptimumSpacerWidth()
        _padding = self._paddings[index]
        return _optWidth + _padding

    def _calcTopLeft(self, index):
        slotSize0 = self.transformAsNeeded(self._slots[index])[0]
        slotStart = self._getChildSlotStart(index)
        slotDelta = slotSize0 * slotStart
        topLeftBorders = (self.borders[0], self.borders[3])
        spacer = 0  # 0 offset from drawable area, NOT parent area
        if (index > 0):
            spacer = sum(self._spacers[0:index])
        top = spacer + slotDelta + topLeftBorders[0]
        left = topLeftBorders[1]
        topLeft = (top, left)
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
        if _sparePixels > 0:
            print(
                "!!! SPARE PIXELS: {sp} on {s}".format(
                    sp=_sparePixels, s=self._spacers
                )
            )
        return _sparePixels

    def _resizeChildren(self):
        childCount = self._childCount()

        if childCount > 0:  # only update when there's children present

            # calc padding
            self._paddings = [
                self._calcPadding(i) for i, c in enumerate(self.children[1:])
            ]
            # calculate real spacers
            self._spacers = [
                    self._calcRealSpacerWidth(i) for i, c in
                    enumerate(self.children[1:])
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

    def _resizeAChild(self, child, index):

        slotSize = self._slots[index]
        topLeft = self._topLefts[index]

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
        if self.drawBorders:
            self._drawBorder(draw)

        # return image rotated to the correct orientation
        return self._image.rotate(-self.rotation_degrees, expand=1)

    def _drawBorder(self, draw):
        w = self.borders[0]
        c = self.borderColour
        while w > 0:
            rectSize = tuple(numpy.subtract(self.size, w))
            w = w - 1
            draw.rectangle([(w, w), rectSize], outline=c, width=1)

        def drawSpacer(w, tl):
            if w > 0:
                if self.packingMode == 'h':
                    tlxy = [tl[0] - w, tl[1]]
                    brxy = [tl[0] - 1, self.size[1] - tl[1]]
                else:
                    tlxy = [tl[0], tl[1] - w]
                    brxy = [self.size[0] - tl[0], tl[1] - 1]
                tlbr = tlxy + brxy
                draw.rectangle(tlbr, fill=c, width=1)

        if len(self._spacers) > 0:
            [
                drawSpacer(w, tl)
                for w, tl
                in zip([0] + self._spacers, self._topLefts)
            ]

    def _drawChildren(self):
        [child._drawChildren() for child in self.children]
        [
            self._drawChildOnParent(child, index)
            for index, child
            in enumerate(self.children)
        ]

    def _drawChildOnParent(self, child, index):
        if not child._image:
            print("WARNING: NO IMAGE ON THIS CHILD", child)
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
