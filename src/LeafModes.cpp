#include <Adafruit_NeoPixel.h>

extern const int NUMBER_OF_LEAVES;
extern const int NUMBER_OF_PIXELS;
extern const int PIXELS_PER_LEAF;
extern volatile boolean mode_changed;;

extern Adafruit_NeoPixel strip;

extern uint32_t RGBtoDecimal(uint8_t, uint8_t, uint8_t);
extern void reverseArray(int[], int);

/*
 * @brief Method for updating the colour of a Leaf
 * @param leafIndex Which Leaf to modify, by index
 * @param colour The colour to use in decimal form, convert using RBGtoDecimal() or hexToDecimal().
 */
void setLeaf(int leafIndex, uint32_t colour) {
  int pixelStartPos = leafIndex * PIXELS_PER_LEAF;
  strip.fill(colour, pixelStartPos, PIXELS_PER_LEAF);
  //strip.show();
}

uint32_t wheel(byte pos) {
  if (pos < 85) {
    return strip.Color(pos * 3, 255 - pos * 3, 0);
  } else if (pos < 170) {
    pos -= 85;
    return strip.Color(255 - pos * 3, 0, pos * 3);
  } else {
    pos -= 170;
    return strip.Color(0, pos * 3, 255 - pos * 3);
  }
}

// Morphing from num1 to num2 in given number of steps
void morphNum(int num1, int num2, int steps, int* output) {
  float slope;
  if (num1 < num2) {
    slope = (float)(num2 - num1) / (steps - 1);
    for (int x = 0; x < steps; x++) {
      output[x] = (int)(slope * x + num1);
    }
  } else if (num1 > num2) {
    slope = (float)(num1 - num2) / (steps - 1);
    for (int x = 0; x < steps; x++) {
      output[x] = (int)(slope * x + num2);
    }
  } else {
    for (int x = 0; x < steps; x++) {
      output[x] = num1;
    }
  }
}

void startupAnimation(int wait) {
  for (int leaf = 0; leaf < NUMBER_OF_LEAVES; ++leaf) {

    if (mode_changed) {
      mode_changed = false;
      break;
    }

    setLeaf(leaf, RGBtoDecimal(255, 0, 255));
    delay(wait);
  }
}

void stripTest(int wait) {
  for (uint16_t j = 0; j < 255; j++) {

    if (mode_changed) {
      mode_changed = false;
      break;
    }

    for (uint16_t i = 0; i < strip.numPixels(); i++) {
      uint16_t pixel_index = (i * 256 / strip.numPixels()) + j;
      strip.setPixelColor(i, wheel(pixel_index & 255));
    }
    strip.show();
    delay(wait);
  }
}

void leafRainbow(int wait) {
  for (uint16_t j = 0; j < 255; j++) {

    if (mode_changed) {
      mode_changed = false;
      break;
    }

    for (uint16_t leafIndex = 0; leafIndex < NUMBER_OF_LEAVES; leafIndex++) {
      uint16_t colorIndex = (leafIndex * 256 / NUMBER_OF_LEAVES) + j;
      setLeaf(leafIndex, wheel(colorIndex & 255));
    }
    strip.show();
    delay(wait);
  }
}

void christmas() {
  // Define the two colors for Christmas (red and green)
  uint32_t colours[2] = { RGBtoDecimal(255, 0, 0), RGBtoDecimal(0, 255, 0) };

  for (uint16_t i = 0; i < NUMBER_OF_LEAVES; i++) {
    
    if (mode_changed) {
      mode_changed = false;
      break;
    }

    setLeaf(i, colours[rand() % 2]);  // Pick a random color from the array
  }
  strip.show();
  delay(0);
}

void rainbowCycle(int wait) {
  for (uint16_t j = 0; j < 255; j++) {

    if (mode_changed) {
      mode_changed = false;
      break;
    }

    uint32_t color = wheel(j);
    strip.fill(color, 0, NUMBER_OF_PIXELS);  // Fills all pixels with the color
    strip.show();
    delay(wait);
  }
}

void whiteColour(int wait, uint8_t r, uint8_t g, uint8_t b) {
  int redSteps[255], greenSteps[255], blueSteps[255];

  morphNum(255, r, 255, redSteps);
  morphNum(255, g, 255, greenSteps);
  morphNum(255, b, 255, blueSteps);

  // Reverse the steps
  reverseArray(redSteps, 255);
  reverseArray(greenSteps, 255);
  reverseArray(blueSteps, 255);

  for (int i = 0; i < 255; i++) {

    if (mode_changed) {
      break;
    }

    strip.fill(RGBtoDecimal(redSteps[i] / 4, greenSteps[i] / 4, blueSteps[i] / 4));
    strip.show();
    delay(wait);
  }

  morphNum(r, 255, 255, redSteps);
  morphNum(g, 255, 255, greenSteps);
  morphNum(b, 255, 255, blueSteps);

  for (int i = 0; i < 255; i++) {

    if (mode_changed) {
      mode_changed = false;
      break;
    }

    strip.fill(RGBtoDecimal(redSteps[i] / 4, greenSteps[i] / 4, blueSteps[i] / 4));
    strip.show();
    delay(wait);
  }
}