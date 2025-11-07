#include <Wire.h>

#define SLAVE_ADDR 0x08   // change this to 0x09, 0x0A, etc. for each board
#define BUTTON_PIN 2

byte buttonState = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Button to GND
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(requestEvent);  // Called when Pi asks for data
}

void loop() {
  buttonState = digitalRead(BUTTON_PIN) == LOW ? 1 : 0;
  delay(50);  // debounce
}

void requestEvent() {
  Wire.write(buttonState);  // Send the state to Pi
}
