// Arduino_0.9.ino
#include <Wire.h>

#define LED_1_PIN 9
#define LED_2_PIN 10
#define LED_3_PIN 11
#define LED_4_PIN 12
#define SPEAKER_PIN 13
#define BUT_PIN 8
#define NUM_LED 4
#define OFF 0
#define SOLID 1
#define BLINK 2
#define ROTATE 3
#define ROTATE_INT 40
#define FREQ 2500
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
byte light_status = OFF, sound_on = 0 ;
int freq = 2500 ;

void SetLEDs(void){
  int i;

  if ( millis()-lastRotate > ROTATE_TIME ){
    lastRotate = millis() ;
    rotateLED = ( rotateLED + 1 ) % NUM_LED ;
    if ( rotateLED == 0 && sound_on ){
      tone ( SPEAKER_PIN, freq ) ;
    } else {
      noTone ( SPEAKER_PIN ) ;
    }
  }
  for ( i = 0 ; i < NUM_LED ; i++ ){
    if ( light_status == ROTATE && i == rotateLED || light_status == SOLID || light_status == BLINK && rotateLED < 2 ){
      digitalWrite ( LED_pin[i], HIGH ) ;
    } else {
      digitalWrite ( LED_pin[i], LOW ) ;
    }
  }
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

  byte sound_stat ;
  //Serial.println(F("LED status received"));
  byte newstat = Wire.read() ;
  if ( newstat == 0xFF ){    // this is the "hello signal, so do nothing"
    speaker = 0 ;
    light_status = OFF ;
  } else {
    light_status = newstat & 0x03 ;  // least 2 significant bits
    sound_stat = (newstat >> 2 ) & 0x03 ;  // next two bits
    freq = 2500 * sound_stat ;
    sound_on = (sound_stat > 0) ;
  }
}
