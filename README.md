# RPi Inky Layout Manager

This is a layout manager I wrote to help me break up the display of a
Pimoroni Inky-pHAT into seperate drawable areas.

You might find other uses for it - let me know if it's handy!


# How it works

Create a new Layout:

    layout = Layout( dimensions, packingMode, border, rotationMode)

where:

* `dimensions` is a 2-part tuple of the form `(width, height)`.
* `packingMode` is the packing direction: currently either `h` (horizontal) or `v` (vertical). 
* `border` is the width of border you want (defaults to `0`).


