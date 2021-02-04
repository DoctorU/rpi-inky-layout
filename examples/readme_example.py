from rpi_inky_layout import Layout, Rotation
from PIL import Image, ImageDraw
# Uncomment if you want to test on your Pi/Inky combo.
# from inky.auto import auto

topLayout = Layout((400, 100), packingMode='h', border=(1, 2))

# Uncomment if you want to test on your Pi/Inky combo.
# board = auto()
# topLayout = Layout(board.resolution, 'h', (0, 0))

sublayout1 = topLayout.addLayer()
sublayout2 = topLayout.addLayer()
sublayout3 = topLayout.addLayer()
sublayout31 = sublayout3.addLayer()
sublayout32 = sublayout3.addLayer()


mode = "P"
bgColour = 0
image31 = Image.new(mode, sublayout31.size, bgColour)
draw = ImageDraw.Draw(image31)
draw.text(tuple(s/2 for s in sublayout31.size), "Hello", 1)
sublayout31.setImage(image31)

image32 = Image.new(mode, sublayout32.size, bgColour)
draw = ImageDraw.Draw(image32)
draw.text(tuple(s/2 for s in sublayout32.size), "World!", 1)
sublayout32.setImage(image32)

topLayout.draw()
topLayout.write("hello-world.png")

# Uncomment if you want to test on your Pi/Inky combo.
# inky_image = Image.open("hello-world.png")
# board.set_image(inky_image)
