from PIL import Image, ImageDraw
from random import randint
import numpy
import pdb

from .rotation import Rotation
from math import floor


"""
    Layout - a simple image layout manager for RPi Inky HATs.
"""


class Layout:

    DEFAULT_PALETTE = (255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252

    @staticmethod
    def tupleReversed(tupleValue):
        return tuple(reversed(tupleValue))

    def __str__(self):
        return "{id}/{depth}/{pb}/{children}:{tl}+{dim}".format(
            id=self._id,
            depth=self._depth,
            tl=self.topLeft,
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
#        if self.rotation.value % 2:
#            self.size = self.tupleReversed(size)
#        else:
        self.size = size
        self.rotation_degrees = self.rotation.value * 90
        self.topLeft = (0, 0)
        self.packingMode = packingMode
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

        self._children = []
        self._spacers = []
        self._slots = []
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

    def resize(self, size):
        size = tuple(round(dim) for dim in size)
        self.size = size
        if self._image:
            self._image = self._image.crop((0, 0) + size)
        self._resizeChildren()

    def _calcDrawableSize(self):
        w, h = self.size
        bt, br, bb, bl = self.borders
        _calcDrawableSize = (w - bl - br, h - bt - bb)
        return _calcDrawableSize

    def _calcSlotWidth(self):
        dw = self._calcDrawableSize()[0]
        sw = self._spacersWidth()
        w = (dw - sw)
        slotCount = self._getChildSlotTotal()
        if slotCount > 0:
#            w = floor(w / slotCount)

            w = (w / slotCount)
        print("slotwidth:{sw},{sw},{w},{sc}".format(dw=dw, sw=sw, w=w, sc=slotCount))
        w = int(w)
        print("slotwidth:{sw},{sw},{w},{sc}".format(dw=dw, sw=sw, w=w, sc=slotCount))
        return w

    def _getSlotWidthFor(self, child):
        return self._calcSlotWidth() * child.packingBias

    def _calcSpacersErrorMargin(self):
        """The additional width to put into the spacers, to even things out."""
        drawableWidth = self._calcDrawableSize()[0]
        childCount = len(self._children)
        _errorWidth = 0
        if childCount > 0:
            _errorWidth = drawableWidth % childCount

        print("childcount:{c} _errorWidth:{e} drawableWidth:{w}".format(
            c=childCount, e=_errorWidth, w=drawableWidth)
        )
        return _errorWidth

    def _calcOptimumSpacerWidth(self):
        bt, br, bb, bl = self.borders
        print("_optimumSpacerWidth:{bl}".format(bl=bl))
        return bl

    def _realSpacerWidth(self, index):
        _optWidth = self._calcOptimumSpacerWidth()
        _errorWidth = 0
        _totalError = self._calcSpacersErrorMargin()
        if index <= _totalError:
            _errorWidth = 1
        print("_realSpacerWidth:opt={o},err={e},totalErr={te}".format(
                o=_optWidth, e=_errorWidth, te=_totalError
            )
        )
        return _optWidth + _errorWidth

    def _spacersWidth(self):
        """The total width of all the spacers."""
        return sum(self._spacers)

    def _spacersWidthFor(self, index):
        return self._spacers[index]

    def _resizeChildren(self):
#        pdb.set_trace()
        childCount = len(self._children)
        self._spacers = []
        self._slots = []
        if childCount > 0:  # only update when there's children present

            # calculate overall drawable size
            size = self._calcDrawableSize()

            # calculate spacers
            self._spacers = [
                    self._realSpacerWidth(i) for i, c in
                    enumerate(self._children[0:-1])
            ]

            slotSize = (self._calcSlotWidth(), size[1])

            # Slots are sized to compensate for packingBias
            def _calcSlotSize(child):
                return (slotSize[0] * child.packingBias, slotSize[1])

            self._slots = [_calcSlotSize(child) for child in self._children]
            print(
                    "size:{s} children:{c}".format(
                        s=self.size,
                        c=len(self._children)
                    ),
                    "borders:{b} _spacers:{sp} _slots:{sl}".format(
                        b=self.borders,
                        sp=self._spacers,
                        sl=self._slots
                    )
            )

#            if self.packingMode == 'v':
#                slotSize = self.tupleReversed(slotSize)
            [
                self._resizeAChild(
                    child,
                    index
                ) for index, child in enumerate(self._children)
            ]

    def _resizeAChild(self, child, index):

        slotSize = self._slots[index]
        # calculate the new top-left FIRST (depends on final slot position)
        spacer = 0
        if (index > 0):
            spacer = sum(self._spacers[0:index])
        left = self.borders[3] + spacer + (slotSize[0] * index)
        topLeft = (left, self.borders[0])

        child.resize(slotSize)
        child.topLeft = topLeft

    def draw(self):
        if not self._image:
            print("creating image", self.imageMode)
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
            print("DRAWING SPACERS")

    def _getChildSlotTotal(self):
        """The total number of slots."""
        return self.getChildSlotCount(self._children)

    @staticmethod
    def getChildSlotCount(childrenList):
        """The count of the slot."""
        packingBias = [child.packingBias for child in childrenList]
        packingCount = sum(packingBias)
        return packingCount

    def _getChildSlotStart(self, index):
        """Which slot this child starts in."""
        return self.getChildSlotCount(self._children[0:index])

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
                print("{id}: {tl}".format(id=child._id, tl=child.topLeft))
                self._image.paste(child._image, child.topLeft)

    def write(self, fp):
        self.draw().convert(mode="RGB").save(fp)
        if self._children:
            [
                child.write(fp.replace(".", "-{i}.".format(i=index)))
                for index, child in enumerate(self._children)
            ]
