from PIL import Image
from io import BytesIO
from picamera import PiCamera
import ST7789

disp = ST7789.ST7789()
disp.Init()
disp.clear()
image = Image.new("RGB", (disp.width, disp.height))
disp.backlight(True)


camera = PiCamera()
camera.resolution = (240, 240)
try:
    while True:
        stream = BytesIO()
        image = camera.capture(stream, format='jpeg')
        disp.image(Image.open(stream))
finally:
    disp.backlight(False)
