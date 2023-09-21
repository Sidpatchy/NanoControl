#ifndef LeafModes_h
#define LeafModes_h

#include <Adafruit_NeoPixel.h>

void setLeaf(int leafIndex, uint32_t colour);

uint32_t wheel(byte pos);

void morphNum(int num1, int num2, int steps, int* output);

void startupAnimation(int wait);

void stripTest(int wait);

void leafRainbow(int wait);

void christmas();

void rainbowCycle(int wait);

void morphNum(int, int, int, int[]);

void whiteColour(int wait, uint8_t r, uint8_t g, uint8_t b);

#endif
