from PIL import Image, ImageDraw

class Layout:

    DEFAULT_PALETTE = (255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252
    def __init__(self, dimensions=(250,122), packingMode='h', border=0, rotation=0):
        self.dimensions = dimensions 
        self._packingMode = packingMode
        self.border = border
        self.rotation = 90*rotationMode
        self._children = []
        self._reset()

    def _reset(self):
        self._image = Image.new("P", self.dimensions, 1)
        self._image.putpalette(self.DEFAULT_PALETTE)
        self._drawable = True;


    def write(self, fp):
        self.draw()
        self._image.save(fp)

    """ 
        get_draw - returns an ImageDraw object for drawing on, only if this has no children.
        Otherwise, throws an exception stating that it can't be drawn on.
    """
    def get_ImageDraw(self):
        if self._children:
            raise Exception("You cannot draw on layers that have children")
        return ImageDraw.Draw(self._image)

    def draw(self):
        self.report("drawing {dim}".format(dim=self.dimensions))
        self._updateChildren()
        return self._image

    def report(self, message):
        print(message)

    def resize(self, dimensions):
        self.dimensions = dimensions
        self._updateChildren()

    def addLayer(self, border=1):
        #add a child Layer to the child list, then resize them all
        childLayer = Layout()
        self._reset()
        self._drawable = False;
        self._children.append(childLayer)
        self._updateChildren()
        self.draw()
        return childLayer

    def _updateChildren(self):
        childCount = len(self._children)
        if childCount > 0:
            if self._packingMode == 'h':
                bordersW = (childCount-1+2) * self.border
                bordersH =  2 * self.border
                newChildW = int(self.dimensions[0]/childCount) - bordersW
                newChildH = int(self.dimensions[1]) - bordersH

            if self._packingMode == 'v':
                bordersW =  2 * self.border
                bordersH = (childCount-1+2) * self.border
                newChildW = int(self.dimensions[0]) - bordersW
                newChildH = int(self.dimensions[1]/childCount) - bordersH

            newChildDims = [(child.resize((newChildW, newChildH)) ) for child in self._children]

            


