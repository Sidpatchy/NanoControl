from sLOUT import readConfig

# Parse data from the config file
num_pixels = readConfig('../config.yml', 'numPixels')
numLeaves = readConfig('../config.yml', 'numLeaves')
neopixelPin = readConfig('../config.yml', 'neopixelPin')

print(neopixelPin)