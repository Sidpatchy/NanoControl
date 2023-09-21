#include "DisplayManager.h"
#include <Adafruit_NeoPixel.h>

extern Adafruit_SH1106G display;

void updateDisplay(String title, 
                   String line0, 
                   String line1, 
                   String line2, 
                   String line3,
                   String line4) 
{
    display.clearDisplay();
    display.setCursor(0,0);
    display.print(title.c_str());
    display.setCursor(0, 10);  // move cursor down by 10 pixels
    display.print(line0.c_str());
    display.setCursor(0, 20);
    display.print(line1.c_str());
    display.setCursor(0, 30);
    display.print(line2.c_str());
    display.setCursor(0, 40);
    display.print(line3.c_str());
    display.setCursor(0, 50);
    display.print(line4.c_str());
    display.display();  // send buffer data to the display
}

void mainPage() {
  updateDisplay("    NanoControl-v2    ", 
                "  Mode Select Screen  ", 
                "LeafR, Rainb, Rand", 
                "Line 2", 
                "Line 3", 
                "Line 4");
}

void displayOff() {
  updateDisplay("", "", "", "", "", "");
}