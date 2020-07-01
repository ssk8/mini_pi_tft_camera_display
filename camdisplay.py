import digitalio
import board
from PIL import Image
import adafruit_rgb_display.st7789 as st7789
from io import BytesIO
from picamera import PiCamera

disp = st7789.ST7789(board.SPI(), rotation=90, width=135, height=240, x_offset=53, y_offset=40, cs=digitalio.DigitalInOut(board.CE0), dc=digitalio.DigitalInOut(board.D25), baudrate=24000000)

stream = BytesIO()
camera = PiCamera()
camera.resolution = (240, 135)
camera.capture(stream, format='jpeg')
#stream.seek(0)
disp.image(Image.open(stream))
