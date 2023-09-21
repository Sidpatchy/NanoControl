#ifndef DisplayManager_h
#define DisplayManager_h

#include <Adafruit_SH110X.h>
#include <Adafruit_NeoPixel.h>

void updateDisplay(String title, 
                   String line0 = "", 
                   String line1 = "", 
                   String line2 = "", 
                   String line3 = "",
                   String line4 = "");

void mainPage();

void displayOff();

#endif
