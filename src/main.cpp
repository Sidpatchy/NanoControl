/*
Adafruit MacroPad (RP2040):
Uses external source for 5v.
Connects to ground through STEMMA QT connector.
Uses pin 21 for LED Pin.
Uses pin "PIN_NEOPIXEL" for keypad LEDs (if desired).

NanoControl v2 - K.I.S.S. Edition
*/

// LIBRARIES
#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <Adafruit_SH110X.h>
#include <RotaryEncoder.h>
#include <NoDelay.h>
#include "pico/multicore.h"

// PROJECT COMPONENTS
#include "DisplayManager.h"
#include "LeafModes.h"

// CONFIGURATION

// Which pin will be used for controlling the LEDs
#define LED_PIN 21

noDelay christmas1(2500, christmas);

#define KEYPAD_LED_PIN 19

// Rotary Encoder Pins
#define PIN_SWITCH 0
#define PIN_ROTA 17
#define PIN_ROTB 18

// Display pins
#define OLED_DC 24
#define OLED_RST 23
#define OLED_CS 22

volatile int PIXELS_PER_LEAF = 12;
volatile int NUMBER_OF_LEAVES = 9;

#define DEFAULT_MODE "rainbow"
#define DEFAULT_BRIGHTNESS 255  // Max is 255

// Do not touch this unless you know what you're doing.

// Create NeoPixel strip for leaves.
volatile int NUMBER_OF_PIXELS = PIXELS_PER_LEAF * NUMBER_OF_LEAVES;
Adafruit_NeoPixel strip(NUMBER_OF_PIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);

// Create NeoPixel strip for keypad.
Adafruit_NeoPixel keypad_strip(12, KEYPAD_LED_PIN, NEO_GRB + NEO_KHZ800);

// Create the OLED display
Adafruit_SH1106G display = Adafruit_SH1106G(128, 64, MOSI, SCK, OLED_DC, OLED_RST, OLED_CS);

// Create the rotary encoder
RotaryEncoder encoder(PIN_ROTA, PIN_ROTB, RotaryEncoder::LatchMode::FOUR3);
void checkPosition() {  encoder.tick(); }
// our encoder position state
int encoder_pos = 0;

volatile boolean mode_changed = true;
typedef struct {
    int mode;
    int wait;
    int brightness;
    uint32_t colour1;
    uint32_t colour2;
    uint32_t colour3;
} Mailbox;

volatile Mailbox mailbox;

/*
 * Init display and related funcitons.
 *
 */
void setup() {
    Serial.begin(9600);

    // Set default mailbox values.
    mailbox.mode = 0;
    mailbox.wait = 0;
    mailbox.brightness = DEFAULT_BRIGHTNESS;
    mailbox.colour1 = 16711680;
    mailbox.colour2 = 0;
    mailbox.colour3 = 0;

    // Init keypad strip to off.
    keypad_strip.begin();
    keypad_strip.show();

    // Enable OLED.
    display.begin(0, true);
    display.display();

    // Set all MacroPad keys to inputs.
    for (uint8_t i=0; i<=12; i++) {
        pinMode(i, INPUT_PULLUP);
    }

    // Set rotary encoder inputs and interrupts.
    pinMode(PIN_ROTA, INPUT_PULLUP);
    pinMode(PIN_ROTB, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(PIN_ROTA), checkPosition, CHANGE);
    attachInterrupt(digitalPinToInterrupt(PIN_ROTB), checkPosition, CHANGE);

    // Text display setup.
    display.setTextSize(1);
    display.setTextWrap(false);
    display.setTextColor(SH110X_WHITE, SH110X_BLACK); // white text, black background
}

int old_pos = 0;

void keyColour();

void encoderHandler();

void keypadHandler();

void displayUpdater();

void DecimalToRGB(uint32_t colour1, uint8_t *string, uint8_t *string1, uint8_t *string2);

/*
 * Handle display and related funcitons.
 *
 */
void loop() {
    // Monitor encoder, change values as needed.
    encoderHandler();

    // Handle updates to the keypad.
    keypadHandler();

    // Handle display update. Update display last
    // to ensure that any interactions are reflected.
    displayUpdater();
}

/*
 * Init leaf-related functions.
 *
 */
void setup1() {
    // Init leaf strip to off.
    strip.begin();
    strip.show();
}

/*
 * Handle leaf-related funcitons.
 *
 */
void loop1() {
    strip.setBrightness(mailbox.brightness);

    switch (mailbox.mode) {
        case -1:
            strip.fill(0);
            strip.show();
            break;
        case 0: // leafRainbow
            leafRainbow(mailbox.wait);
            break;
        case 1: // christmas
            christmas1.update();
            christmas1.setdelay(2500);
            break;
        case 2: // rainbowCycle
            rainbowCycle(mailbox.wait);
            break;
        case 3: // whiteColour
            uint8_t r;
            uint8_t g;
            uint8_t b;

            DecimalToRGB(mailbox.colour1, &r, &g, &b);

            whiteColour(mailbox.wait, r, g, b);
            break;
    }
}

void displayUpdater() {
    if (mailbox.mode + 1 == 0) {
        displayOff();
    }
    else {
        mainPage();
    }
}

void encoderHandler() {
    // Encoder related functions
    encoder.tick();
    encoder_pos = encoder.getPosition() * -1; // invert rotation direction.

    if (digitalRead(PIN_SWITCH) && encoder_pos != old_pos) {
        // Determine the difference between current value and previous value
        int16_t encoder_pos_difference = encoder_pos - old_pos;

        // Update the mailbox brightness with the new value applied
        // Check for potential overflows or underflows
        int16_t new_brightness = mailbox.brightness + (encoder_pos_difference * 5);

        // Ensure new brightness is within bounds (0-255)
        if (new_brightness <= 0) {
            mailbox.brightness = 1;
        } else if (new_brightness > 255) {
            mailbox.brightness = 255;
        } else {
            mailbox.brightness = new_brightness;
        }

        strip.setBrightness(mailbox.brightness);
        keypad_strip.setBrightness(mailbox.brightness);

        Serial.print("\n\nBrightness: ");
        Serial.print(mailbox.brightness);

        old_pos = encoder_pos;
    }
}

void keypadHandler() {
    for (int i=1; i<=12; i++) {
        if (!digitalRead(i)) { // switch pressed!
            Serial.print("Switch "); Serial.println(i);

            // Prevent flickering of animations if keyswitch is held down.
            if (mailbox.mode != i-2) {

                // Update mailbox
                mailbox.mode = i-2;
                mode_changed = true;

                /*
                 * Ensure that this method is run instantly by core 1.
                 *
                 * There is a known bug that ocurrs when switching from
                 * off directly to christmas where this fix does not
                 * seem to work for some reason.
                 */
                christmas1.setdelay(0);
            }
        }

        keyColour();

        /*
        // Check if keys should be lit
        if (mailbox.mode +2 == i) {
          keypad_strip.setPixelColor(i-1, 0xFFFFFF);  // make white
        }
        else {
          keypad_strip.setPixelColor(i-1, 0); // turn off pixel
        }
        */
    }
    keypad_strip.show();
}

void keyColour() {
    int activeKey = mailbox.mode + 1;
    static byte colorIndex = 0;  // this will hold the current color index
    static unsigned long lastRun = millis();

    switch (activeKey) {
        case 0: //off
            keypad_strip.fill(0);
            keypad_strip.setPixelColor(activeKey, 0);
            break;
        case 1: // leafrainbow
            if (lastRun - millis() > 25) {
                keypad_strip.fill(0);

                uint32_t color = wheel(colorIndex);
                keypad_strip.setPixelColor(activeKey, color);
                colorIndex++;  // increment the color index for next time
                if(colorIndex > 254) {  // Reset when it exceeds 254, to avoid overflow
                    colorIndex = 0;
                }
                lastRun = millis();
            }
            break;
        case 2 ... 11: // christmas
            keypad_strip.fill(0);
            keypad_strip.setPixelColor(activeKey, 0xFFFFFF);
            break;
    }
}

/*
 * @brief Method for converting RGB to decimal.
 * @param r Red value
 * @param g Green value
 * @param b Blue value
 */
uint32_t RGBtoDecimal(uint8_t r, uint8_t g, uint8_t b) {
    uint32_t decimalValue;

    decimalValue = r;
    decimalValue = (decimalValue << 8) + g;
    decimalValue = (decimalValue << 8) + b;

    return decimalValue;
}

/*
 * @brief Method for converting a decimal value to RGB.
 * @param decimalValue The decimal value representing the RGB color.
 * @param r Pointer to store the extracted Red value.
 * @param g Pointer to store the extracted Green value.
 * @param b Pointer to store the extracted Blue value.
 */
void DecimalToRGB(uint32_t decimalValue, uint8_t* r, uint8_t* g, uint8_t* b) {
    *b = decimalValue & 0xFF;              // Extract the last 8 bits for blue
    *g = (decimalValue >> 8) & 0xFF;       // Extract the next 8 bits for green
    *r = (decimalValue >> 16) & 0xFF;      // Extract the next 8 bits for red
}


/*
 * @brief Method for converting hex RGB codes to decimal.
 * @param hexColour colour value in hex.
 */
uint32_t hexToDecimal(const char* hexColour) {
    // Assuming hexColour is in the format "#RRGGBB"
    if (hexColour[0] != '#') return 0;  // Invalid format

    long number = strtol(&hexColour[1], NULL, 16);  // Convert hex string to a long integer
    return (uint32_t)number;
}

void reverseArray(int* arr, int length) {
    int start = 0;
    int end = length - 1;
    while (start < end) {
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}