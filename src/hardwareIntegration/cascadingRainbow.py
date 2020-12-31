import time
import board
import neopixel
from sLOUT import readConfig

# Parse data from the config file
num_pixels = readConfig('config.yml', 'numPixels')
numLeaves = readConfig('config.yml', 'numLeaves')
neopixelPin = readConfig('config.yml', 'neopixelPin')

pixels = neopixel.NeoPixel(neopixelPin, num_pixels)

ORDER = neopixel.RGB

def wheel(pos):
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

def cascadingRainbow(wait, difBetweenLeaves):
    # starts at one rather than 0
    for j in range(255):
        for i in range(1):
            pixel_index = (i * 256 // num_pixels) + j
            leaf = 0
            for leaf in range(numLeaves):
                pixels[0 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[1 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[2 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[3 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[4 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[5 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[6 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[7 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[8 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[9 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[10 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                pixels[11 + (leaf * 12)] = wheel((pixel_index - (20 * leaf)) & 255)
                if leaf > numLeaves:
                    leaf = 0
                else:
                    leaf = leaf + 1
            
        pixels.show()
        time.sleep(wait)