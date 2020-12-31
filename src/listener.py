# Import as few modules as possible to conserve memory
import board
import neopixel
from sLOUT import readConfig
from time import sleep
from random import randint
from morphNum import morphNum
import asyncio
import random
#from hardwareIntegration.rainbow import rainbowCycle
#from hardwareIntegration.cascadingRainbow import cascadingRainbow
#from hardwareIntegration.stripTest import stripTest

num_pixels = readConfig('config.yml', 'numPixels')
numLeaves = readConfig('config.yml', 'numLeaves')
neopixelPin = readConfig('config.yml', 'neopixelPin')

pixels = neopixel.NeoPixel(board.D18, num_pixels)

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

def stripTest(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        sleep(wait)

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
        sleep(wait)

def rainbowCycle(wait):
    for j in range(255):
        for i in range(1):
            pixel_index = (i * 256 // num_pixels) + j
            pixels.fill(wheel(pixel_index))
        #pixels.fill()
        sleep(wait)

def fastRainbowCycle(wait):
    for j in range(255):
        for i in range(1):
            pixel_index = (i * 256 // num_pixels) + j
            pixels.fill(wheel(pixel_index & 255))
        #pixels.fill()
        sleep(wait)

def heartbeat(wait):
    colourOne = [0, 0, 0]
    colourTwo = [0, 255, 128]
    workingColor = colourOne
    colourOpposite = colourTwo

    if max(colourOne) >= max(colourTwo):
        peak = max(colourOne)
    else: 
        peak = max(colourTwo)

    for i in range(peak*2):
        if i < 256:
            print('fuck')
            # Cycle through red
            if workingColor[0] >= colourOpposite[0]:
                workingColor[0] = colourOpposite[0]
            else:
                workingColor[0] = workingColor[0] + 1

            # Cycle through green
            if workingColor[1] >= colourOpposite[1]:
                workingColor[1] = colourOpposite[1]
            else:
                workingColor[1] = workingColor[1] + 1

            # Cycle through blue
            if workingColor[2] >= colourOpposite[2]:
                workingColor[2] = colourOpposite[2]
            else:
                workingColor[2] = workingColor[2] + 1

            colour = (workingColor[0], workingColor[1], workingColor[2])
            pixels.fill(colour)
            
            if workingColor == colourTwo:
                colourOpposite = colourOne

        else:
            print('shit')
            # Cycle through red
            if colourOpposite[0] >= workingColor[0]:
                workingColor[0] = colourOpposite[0]
            else:
                workingColor[0] = workingColor[0] - 1

            # Cycle through green
            if colourOpposite[1] >= workingColor[1]:
                workingColor[1] = colourOpposite[1]
            else:
                workingColor[1] = workingColor[1] - 1

            # Cycle through blue
            if colourOpposite[2] >= workingColor[2]:
                workingColor[2] = colourOpposite[2]
            else:
                workingColor[2] = workingColor[2] - 1

            colour = (workingColor[0], workingColor[1], workingColor[2])
            pixels.fill(colour)

            if workingColor == colourOpposite:
                colourOpposite = colourTwo

    # Switch colour opposite to colourOne after the loop has run
#    if colourOpposite == colourTwo:
#        colourOpposite = colourOne
#        workingColor = colourTwo
#    elif colourOpposite == colourOne:
#        colourOpposite = colourTwo
#        workingColor = colourOne

# A better name would be good
def col1WhiteCol2White(wait, colour1, colour2):
    
    # Go from white to colour1
    redSteps = morphNum(256, colour1[0], 256)
    greenSteps = morphNum(256, colour1[1], 256)
    blueSteps = morphNum(256, colour1[2], 256)
    # Reverse the lists
    redSteps.reverse()
    greenSteps.reverse()
    blueSteps.reverse()
    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        pixels.fill((redSteps[i] / 2, greenSteps[i] / 2, blueSteps[i] / 2))
        sleep(wait)
    
    # Go from colour1 to white
    redSteps = (morphNum(colour1[0], 256, 256))
    greenSteps = (morphNum(colour1[1], 256, 256))
    blueSteps = (morphNum(colour1[2], 256, 256))
    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        pixels.fill((redSteps[i] / 2, greenSteps[i] / 2, blueSteps[i] / 2))
        sleep(wait)

    # Go from white to colour2
    redSteps = morphNum(colour2[0], 256, 256)
    greenSteps = morphNum(colour2[1], 256, 256)
    blueSteps = morphNum(colour2[2], 256, 256)
    # Reverse the lists
    redSteps.reverse()
    greenSteps.reverse()
    blueSteps.reverse()
    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        pixels.fill((redSteps[i] / 2, greenSteps[i] / 2, blueSteps[i] / 2))
        sleep(wait)

    # Go from colour2 to white
    redSteps = (morphNum(colour2[0], 256, 256))
    greenSteps = (morphNum(colour2[1], 256, 256))
    blueSteps = (morphNum(colour2[2], 256, 256))
    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        pixels.fill((redSteps[i] / 2, greenSteps[i] / 2, blueSteps[i] / 2))
        sleep(wait)

def whiteColour(wait, colour1):
    # Go from white to colour1
    redSteps = morphNum(256, colour1[0], 256)
    greenSteps = morphNum(256, colour1[1], 256)
    blueSteps = morphNum(256, colour1[2], 256)
    # Reverse the lists
    redSteps.reverse()
    greenSteps.reverse()
    blueSteps.reverse()
    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        pixels.fill((redSteps[i] / 4, greenSteps[i] / 4, blueSteps[i] / 4))
        sleep(wait)
    
    # Go from colour1 to white
    redSteps = (morphNum(colour1[0], 256, 256))
    greenSteps = (morphNum(colour1[1], 256, 256))
    blueSteps = (morphNum(colour1[2], 256, 256))
    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        pixels.fill((redSteps[i] / 4, greenSteps[i] / 4, blueSteps[i] / 4))
        sleep(wait)

def cascadingWhiteColour(wait, colour1):
    # Go from white to colour1
    redSteps = morphNum(256, colour1[0], 256)
    greenSteps = morphNum(256, colour1[1], 256)
    blueSteps = morphNum(256, colour1[2], 256)
    # Reverse the lists
    redSteps.reverse()
    greenSteps.reverse()
    blueSteps.reverse()

    for i in range(256):
        print((redSteps[i], greenSteps[i], blueSteps[i]))
        for leaf in range(numLeaves): 
            morphWhiteCol1 = (redSteps[randint(0, 255)] / 4, greenSteps[randint(0, 255)] / 4, blueSteps[randint(0, 255)] / 4)
            setLeaf(leaf, morphWhiteCol1)
        sleep(wait)

def christmas(wait):
    #colours = [(245, 98, 77), (204, 35, 30), (52, 166, 95), (15, 138, 95), (35, 94, 111)]
    colours = [(255, 0, 0), (0, 255, 0)]
    for i in range(numLeaves):
        setLeaf(i, colours[randint(0,1)])
    sleep(wait)

# Because the Python library sucks
def setLeaf(leafIndex, colour):
    pixels[0 + (leafIndex * 12)] = (colour)
    pixels[1 + (leafIndex * 12)] = (colour)
    pixels[2 + (leafIndex * 12)] = (colour)
    pixels[3 + (leafIndex * 12)] = (colour)
    pixels[4 + (leafIndex * 12)] = (colour)
    pixels[5 + (leafIndex * 12)] = (colour)
    pixels[6 + (leafIndex * 12)] = (colour)
    pixels[7 + (leafIndex * 12)] = (colour)
    pixels[8 + (leafIndex * 12)] = (colour)
    pixels[9 + (leafIndex * 12)] = (colour)
    pixels[10 + (leafIndex * 12)] = (colour)
    pixels[11 + (leafIndex * 12)] = (colour)
    pixels.show()

while True:
    powered = readConfig('hardwareIntegration/status.yml', 'powered')
    mode = readConfig('hardwareIntegration/status.yml', 'mode')

    if powered:
        if mode == 'rainbow':
            rainbowCycle(0.1)
        elif mode == 'fastRainbow':
            fastRainbowCycle(0.001)
        elif mode == 'cascadingRainbow':
            cascadingRainbow(0.001, 20)
            pixels.show()
        elif mode == 'stripTest':
            stripTest(0.001)
        elif mode == 'heartbeat':
            heartbeat(0.001)
        elif mode == 'notSure':
            col1WhiteCol2White(.001, [255, 0, 0], [0, 255, 0])
        elif mode == 'notSure2':
            whiteColour(.1, [16, 255, 16])
        elif mode == 'cascadingWhiteColour':
            cascadingWhiteColour(1, [16, 255, 16])
        elif mode == 'christmas':
            christmas(1)
    elif not powered:
        print('Inactive... sleeping for 1 second to reduce clock cycles.' )
        pixels.fill((0, 0, 0))
        sleep(1)