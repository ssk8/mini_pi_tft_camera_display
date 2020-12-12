import RPi.GPIO as GPIO
import spidev
import numpy as np


class ST7789(object):
    """Adafruit Mini PiTFT 1.3" - 240x240 TFT Add-on for Raspberry Pi, mostly refactored www.waveshare.com demo code"""

    def __init__(self, spi=spidev.SpiDev(0, 0), dc=25, bl=22, A=23, B=24):
        self.width = 240
        self.height = 240
        self._dc = dc
        self._bl = bl
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._dc, GPIO.OUT)
        GPIO.setup(self._bl, GPIO.OUT)
        GPIO.output(self._bl, GPIO.HIGH)
        GPIO.setup(A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self._spi = spi
        self._spi.max_speed_hz = 40000000
        self._buttonA = A
        self._buttonB = B

    @property
    def buttonA(self):
        return GPIO.input(self._buttonA) == GPIO.LOW

    @property
    def buttonB(self):
        return GPIO.input(self._buttonB) == GPIO.LOW

    def backlight(self, val):
        if val:
            GPIO.output(self._bl, GPIO.HIGH)
        else:
            GPIO.output(self._bl, GPIO.LOW)

    """    Write register address and data     """
    def command(self, cmd):
        GPIO.output(self._dc, GPIO.LOW)
        self._spi.writebytes([cmd])

    def data(self, val):
        GPIO.output(self._dc, GPIO.HIGH)
        self._spi.writebytes([val])

    def Init(self):
        self.command(0x36)
        self.data(0x70)

        self.command(0x3A) 
        self.data(0x05)

        self.command(0xB2)
        self.data(0x0C)
        self.data(0x0C)
        self.data(0x00)
        self.data(0x33)
        self.data(0x33)

        self.command(0xB7)
        self.data(0x35) 

        self.command(0xBB)
        self.data(0x19)

        self.command(0xC0)
        self.data(0x2C)

        self.command(0xC2)
        self.data(0x01)

        self.command(0xC3)
        self.data(0x12)   

        self.command(0xC4)
        self.data(0x20)

        self.command(0xC6)
        self.data(0x0F) 

        self.command(0xD0)
        self.data(0xA4)
        self.data(0xA1)

        self.command(0xE0)
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0D)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2B)
        self.data(0x3F)
        self.data(0x54)
        self.data(0x4C)
        self.data(0x18)
        self.data(0x0D)
        self.data(0x0B)
        self.data(0x1F)
        self.data(0x23)

        self.command(0xE1)
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0C)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2C)
        self.data(0x3F)
        self.data(0x44)
        self.data(0x51)
        self.data(0x2F)
        self.data(0x1F)
        self.data(0x1F)
        self.data(0x20)
        self.data(0x23)
        self.command(0x21)

        self.command(0x11)

        self.command(0x29)

    def set_window(self, Xstart, Ystart, Xend, Yend):
#       set the X coordinates
        self.command(0x2A)
        self.data(0x00)               # Set the horizontal starting point to the high octet
        self.data(Xstart & 0xff)      # Set the horizontal starting point to the low octet
        self.data(0x00)               # Set the horizontal end to the high octet
        self.data((Xend - 1) & 0xff)  # Set the horizontal end to the low octet 
#       set the Y coordinates
        self.command(0x2B)
        self.data(0x00)
        self.data((Ystart & 0xff))
        self.data(0x00)
        self.data((Yend - 1) & 0xff)

        self.command(0x2C)   

    def image(self, Image):
        imwidth, imheight = Image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = np.asarray(Image)
        pix = np.zeros((self.width, self.height, 2), dtype=np.uint8)
        pix[..., [0]] = np.add(np.bitwise_and(img[..., [0]], 0xF8), np.right_shift(img[..., [1]], 5))
        pix[..., [1]] = np.add(np.bitwise_and(np.left_shift(img[..., [1]], 3), 0xE0), np.right_shift(img[..., [2]], 3))
        pix = pix.flatten().tolist()
        self.set_window(0, 0, self.width, self.height)
        GPIO.output(self._dc,GPIO.HIGH)
        for i in range(0,len(pix),4096):
            self._spi.writebytes(pix[i:i+4096])		

    def clear(self):
        _buffer = [0xff]*(self.width * self.height * 2)
        self.set_window(0, 0, self.width, self.height)
        GPIO.output(self._dc, GPIO.HIGH)
        for i in range(0, len(_buffer), 4096):
            self._spi.writebytes(_buffer[i:i+4096])		
