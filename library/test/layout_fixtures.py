from rpi_inky_layout import Layout

# A file of pre-defined layout fixtures to re-use in tests.
def childlessLayout(size=(200, 100), border=0, packingMode='h'):
    return Layout(size, packingMode=packingMode, border=border)

def layoutWithLayers(size, count, border=0, packingMode='h'):
    layout = Layout(size, packingMode=packingMode, border=border)
    [layout.addLayer() for i in range(count)]
    return layout

def oneLayerH(size=(97, 85), border=0):
    return layoutWithLayers(size, 1, border)

def twoLayersH(size=(219, 100), border=0):
    return layoutWithLayers(size, 2, border)

def threeLayersH(size=(200, 100), border=0):
    return layoutWithLayers(size, 3, border)

def fourLayersH(size=(203, 100), border=0):
    return layoutWithLayers(size, 4, border)

def fiveLayersH(size=(197, 100), border=0):
    return layoutWithLayers(size, 5, border)

def sixLayersH(size=(197,100), border=0):
    return layoutWithLayers(size, 6, border)
