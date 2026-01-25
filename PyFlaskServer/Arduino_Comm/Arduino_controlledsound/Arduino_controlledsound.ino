// Arduino_controlledsound.ino
#include <Wire.h>

#define LED_1_PIN 9
#define LED_2_PIN 10
#define LED_3_PIN 11
#define LED_4_PIN 12
#define SPEAKER_PIN 13
#define BUT_PIN 8
#define NUM_LED 4
#define ROTATE 1
#define ROTATE_INT 40
#define FREQ 5000
// Arduino pins used for the DIP switches
#define S1 4
#define S2 5
#define S3 6
#define S4 7
#define MIN_BOUNCE 250
#define ROTATE_TIME 100

byte currentButtonState = LOW, newState = LOW;
unsigned long lastTime = 0, curTime = 0, lastRotate = 0, rotateLED = 0 ;
int currentLED = 0, sent = 0 ;
int LED_pin[NUM_LED] = {LED_1_PIN, LED_2_PIN, LED_3_PIN, LED_4_PIN} ;
int speaker = 0 ;

byte status = 0 ;

void SetLEDs(void){
  int i;

  #if ROTATE == 1
  if ( millis()-lastRotate > ROTATE_TIME ){
    lastRotate = millis() ;
    rotateLED = ( rotateLED + 1 ) % NUM_LED ;
    if ( rotateLED == 0 && speaker ){
      tone ( SPEAKER_PIN, FREQ ) ;
    } else {
      noTone ( SPEAKER_PIN ) ;
    }
  }
  for ( i = 0 ; i < NUM_LED ; i++ ){
    if ( i == rotateLED ){
      digitalWrite ( LED_pin[i], status ) ;
    } else {
      digitalWrite ( LED_pin[i], LOW ) ;
    }
  }

  #else

  for ( i = 0 ; i < NUM_LED ; i++ ){
     digitalWrite ( LED_pin[i], status ) ;
   }
  // digitalWrite(LED_1_PIN, (status & 0x01) ? HIGH : LOW );
  // digitalWrite(LED_2_PIN, (status & 0x02) ? HIGH : LOW );
  // digitalWrite(LED_3_PIN, (status & 0x04) ? HIGH : LOW );
  // digitalWrite(LED_4_PIN, (status & 0x08) ? HIGH : LOW );
  //Serial.println ( status ) ;
  #endif
 
}

void powerOffAllLEDs()
{
  digitalWrite(LED_1_PIN, LOW);
  digitalWrite(LED_2_PIN, LOW);
  digitalWrite(LED_3_PIN, LOW);
  digitalWrite(LED_4_PIN, LOW);
}

void setup() {
  pinMode(S1, INPUT_PULLUP);
  pinMode(S2, INPUT_PULLUP);
  pinMode(S3, INPUT_PULLUP);
  pinMode(S4, INPUT_PULLUP);

  
  //Serial.begin ( 9600 ) ;
  int s1state = !digitalRead(S1);
  int s2state = !digitalRead(S2);
  int s3state = !digitalRead(S3);
  int s4state = !digitalRead(S4);

  int I2C_SLAVE_ADD = 0x08 + s4state + 2*s3state + 4*s2state + 8*s1state;
  //Serial.println(I2C_SLAVE_ADD);

  Wire.begin(I2C_SLAVE_ADD);
  pinMode(LED_1_PIN, OUTPUT);
  pinMode(LED_2_PIN, OUTPUT);
  pinMode(LED_3_PIN, OUTPUT);
  pinMode(LED_4_PIN, OUTPUT);
  pinMode(BUT_PIN, INPUT);
  pinMode(SPEAKER_PIN, OUTPUT);

  powerOffAllLEDs();

  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);

}

void loop() {
 
  // first get the button status, and debounce if necessary
  newState = digitalRead(BUT_PIN) ;
  curTime = millis() ;
  if ( newState != currentButtonState && curTime - lastTime >= MIN_BOUNCE && sent == 1 ){
    currentButtonState = newState ;
    lastTime = curTime ;
    sent = 0 ;
    //Serial.print(F("New button state: "));
    //Serial.println(newState);
  }
  SetLEDs ( ) ;
  
}

int Led_no = 0;

void requestEvent(){
  //Serial.println(F("Request Received"));
  //Serial.print(F("sending button state: "));
  //byte readValue = digitalRead(BUT_PIN);
  //Serial.println(readValue);
  Wire.write(currentButtonState);
  sent = 1 ;
}

void receiveEvent(int numBytes){
  //Serial.println(F("LED status received"));
  byte newstat = Wire.read(), lights, sound ;
  if ( newstat == 0xFF ){    // this is the "hello signal, so do nothing"
    speaker = 0 ;
  } else {
      lights = newstat & 0x0F ;
      sound = newstat >> 6 ;  // sound is bit 6 (one from left)
      if ( lights != status ){
        if ( lights == 0 ){
          //Serial.println (F("New status: 0")) ;
        } else {
          //Serial.println (F("New status: 1") ) ;
        }
        status = lights ;
      }
    speaker = sound ;
  }
}

/*
I2C command byte layout (newstat):
  bits [3:0] = lights bitmask (b0..b3)
      b0 -> LED_1_PIN (9)
      b1 -> LED_2_PIN (10)
      b2 -> LED_3_PIN (11)
      b3 -> LED_4_PIN (12)
  bits [7:6] = sound (0..3). In this sketch: speaker ON if nonzero.

OPEN DESIGN QUESTION:
  When ROTATE == 1, how should 'lights' bitmask be interpreted?

  A) Rotate through ONLY the LEDs selected by the bitmask.
     Example: lights=0b0101 -> rotate LED1, LED3, repeat.

  B) Ignore which LEDs are selected, and treat lights as a boolean:
     lights==0 -> rotation OFF, lights!=0 -> rotate all LEDs.

  C) No rotation intended: ROTATE should be 0 and bitmask should map 1:1 to LEDs.
*/


// #define ROTATE_MODE 1
// ROTATE_MODE meanings:
// 0 = No rotation. status bitmask maps directly to LEDs.
// 1 = Rotate all LEDs if status != 0 (status used as ON/OFF only).
// 2 = Rotate only LEDs selected by status bitmask (most “bitmask-consistent”).