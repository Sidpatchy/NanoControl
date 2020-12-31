import time
import board
import neopixel
from sLOUT import readConfig

def wheel(pos):
    ORDER = neopixel.RGB
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbowCycle(wait, pixels, num_pixels):
    for j in range(255):
        for i in range(1):
            pixel_index = (i * 256 // num_pixels) + j
            pixels.fill(wheel(pixel_index & 255))
        #pixels.fill()
        time.sleep(wait)
        return(pixels)