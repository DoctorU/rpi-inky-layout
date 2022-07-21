# RPi Inky Layout Manager

This is a layout manager I wrote to help me break up the display of a
Pimoroni Inky-pHAT into seperate drawable areas.

You might find other uses for it - let me know if it's handy!

[rpi-inky-layout at the Python Package Index](https://pypi.org/project/rpi-inky-layout/)

## Repository Status

![Upload Python Package](https://github.com/DoctorU/rpi-inky-layout/workflows/Upload%20Python%20Package/badge.svg)
![Test Python package](https://github.com/DoctorU/rpi-inky-layout/workflows/Python%20package/badge.svg)

## Outline process

The outline process is:

1. Use the `Layout` class to create a top-level Layout object.
1. Next, add new layers to a `Layout` - it automatically resizes the other `Layout`s at the same level.
1. Take each added sublayer `Layout`, and use its `size` to define a new PIL `Image` to draw on.
1. Draw on the image, Set the `Image` on the appropriate `Layout`.
1. Invoke the top-level `Layout`'s `draw()` method to merge them all together, drawing borders as necessary.

And you end up with a nicely-spaced regions.

# How it works

Create a new Layout:

    layout = Layout( size, packingMode, border)

where:

* `size` is a 2-part tuple of the form `(width, height)`.
* `packingMode` is the packing direction: currently either `h` (horizontal) or `v` (vertical).
* `border` is either a) the width of border (colour defaults to `2`) or b) a 2-tuple containing `(width, colour)`.

Next, add multiple sub-layouts to `layout`

    sublayout1 = layout.addLayer()
    sublayout2 = layout.addLayer()

Then, for leach sublayout, use `sublayout.size` as the size of the image to draw on.

    im1 = Image.new(mode, sublayout1.size, bgColour)
    ...

Draw on the image; Set it back on the sublayout:

    sublayout1.setImage(im1)
    ...

And finally, draw the top level layout and write to file:

    layout.draw()
    layout.write(filename)

You can then do what you want with the file, e.g., load it onto an [Inky display using `setImage`](https://github.com/pimoroni/inky#set-image)
# Detailed usage example

Here's a detailed example.

## Install

Assuming you already have pip3 installed:

    python3 -m pip install rpi-inky-layout

And of course, later upgrade with:

    python3 -m pip install --upgrade rpi-inky-layout

Ready to use!


## Prerequisites

Import the core classes from `rpi_inky_layout` package:

    from rpi_inky_layout import Layout, Rotation

You will also need some sort of image manipulation library, such as
[pillow](https://pillow.readthedocs.io/en/stable/reference/index.html)
(and `rpi-inky-layout` uses the `pillow` library internally anyway):

    from PIL import Image, ImageDraw

Optionally, if you're using it with
[Pimoroni's Inky display library](https://github.com/pimoroni/inky)
(its original purpose), then you will probably want to import that, too:

    from inky.auto import auto


## Create new Layers

Create the top-level `Layout`:

    topLayout = Layout((400, 100), packingMode='h', border=(1, 2))

Or, if you're using your the `inky` library:

    board = auto()
    topLayout = Layout(board.resolution, 'h', (0, 0))


Add as many new layers as you want:

    sublayout1 = topLayout.addLayer()
    sublayout2 = topLayout.addLayer()
    sublayout3 = topLayout.sddLayer()
    sublayout31 = sublayout3.addLayer()
    sublayout32 = sublayout3.addLayer()

Use the sub-layouts to create images:

    mode = "P"
    bgColour = 0
    image31 = Image.new(mode, sublayout31.size, bgColour)
    draw = ImageDraw.Draw(image31)
    draw.text(tuple(s/2 for s in sublayout31.size), "Hello",1)
    sublayout31.setImage(image31)

    image32 = Image.new(mode, sublayout32.size, bgColour)
    draw = ImageDraw.Draw(image32)
    draw.text(tuple(s/2 for s in sublayout32.size), "World!",1)
    sublayout32.setImage(image32)

    topLayout.draw()
    topLayout.write("hello-world.png")

If you're using the Inky, you can load the image up:

    inky_image = Image.open("hello-world.png")
    board.set_image(inky_image)

And you're done!

# Advanced Features

## Alternate Packing Mode

Alternate packing mode is an implicit mechanism.
You can specify a different `packingMode` in the `addLayer` method:

    layout.addLayer(packingMode='v')

By default Layouts added using `addLayer` inherit their parent's packing mode.

### Alternate Packing Mode example


![Fig1: Alternate Packing Mode example](/doc/img/examples/alternatePackingMode.png)

_Figure 1.1: Alternate Packing Mode example.
Three Layout layers are illustrated, each with different packing modes.
The top Layout uses `packingMode='h'`, the left Layout also uses
`packingMode='h'`, and the right Layout uses `packingMode='v'`._

## Rotation

If you want to render the Layout in a rotated orientation, you can set the
Rotation parameter. It takes the values:
 * UP - normal, no rotation; (Default behaviour)
 * LEFT - rotation by -90 or 270 degrees
 * RIGHT - rotation by +90 degrees
 * DOWN - rotated 180 degrees (up side down)

### Rotation examples
For all the following rotation examples, `packingMode='v'`.

![Rotation.UP (the default)](/doc/img/examples/rotation_UP.png)

_Figure 2.1 Rotation.UP (the default)_

![Rotation.LEFT](/doc/img/examples/rotation_LEFT.png)

_Figure 2.2: Rotation.LEFT_

![Rotation.DOWN](/doc/img/examples/rotation_DOWN.png)

_Figure 2.3: Rotation.DOWN_

![Rotation.RIGHT](/doc/img/examples/rotation_RIGHT.png)

_Figure 2.4: Rotation.RIGHT_


## Packing Bias

When adding a layer, you can specify packing bias:

    layout = new Layout()
    sublayout1 = layout.addLayer(packingBias=3)
    sublayout2 = layout.addLayer()  # default packingBias=1

In this example, `sublayout1` will take up 3/4s of the space (3/(1+3)),
while `sublayout2` will be left with the remaining 1/4.

### Packing Bias example

![packingBias=3](/doc/img/examples/packingBias.png)

_Figure 3.1: Two layers, the first uses the default `packingBias`,
the second uses `packingBias=3`._

## Subclass `Layout` and add it as a child

Subclassing the Layout class allows you to create pre-decorated layouts, which
dynamically re-draw themselves.
Ensure that `Layout.__init__()` is called from your
subclass's constructor method. Implement the default draw behaviour
by overriding the `Layout.drawOverride(self)` method, too. Remember that this
method is called after resizing, so you should be able to resize the
information that you display at runtime.

    layout = new Layout()
    child = new DynamicLayout()  # your subclass, overrides `Layout.draw()`
    layout.addLayout(child)  # returns child, resized. will be auto-redrawn.
