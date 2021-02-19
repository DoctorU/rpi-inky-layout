from rpi_inky_layout import Layout, Rotation


# A file of pre-defined layout fixtures to re-use in tests.
def childlessLayout(size=(200, 100), border=0, packingMode='h'):
    return Layout(size, packingMode=packingMode, border=border)


def layoutWithLayers(
        size,
        count,
        border=0,
        packingMode='h',
        rotation=Rotation.UP
):
    layout = Layout(
        size,
        packingMode=packingMode,
        border=border,
        rotation=rotation
    )
    [layout.addLayer() for i in range(count)]
    return layout


def oneLayer(size=(97, 85), border=0, packingMode='h'):
    return layoutWithLayers(size, 1, border, packingMode=packingMode)


def twoLayers(size=(219, 100), border=0, packingMode='h'):
    return layoutWithLayers(size, 2, border, packingMode=packingMode)


def threeLayers(
        size=(200, 100),
        border=0,
        packingMode='h',
        rotation=Rotation.UP
):
    return layoutWithLayers(
        size, 3, border,
        packingMode=packingMode, rotation=rotation
    )


def fourLayers(size=(203, 100), border=0, packingMode='h'):
    return layoutWithLayers(size, 4, border, packingMode=packingMode)


def fiveLayers(size=(197, 100), border=0, packingMode='h'):
    return layoutWithLayers(size, 5, border, packingMode=packingMode)


def sixLayers(size=(197, 100), border=0, packingMode='h'):
    return layoutWithLayers(size, 6, border, packingMode=packingMode)
