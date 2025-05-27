#include <ArduinoJson.h>
#include <DHT.h>


const int trigPin = 22;
const int echoPin = 23;
const int statusLED = 3;

const int DHTPin = 2;

DHT dht(DHTPin, DHT22);

StaticJsonDocument<200> doc;

float getDistance(){

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  return (pulseIn(echoPin, HIGH) * 0.0343) / 2;    // divided by 2 to take into account just going or coming back, not whole time.
}




void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(statusLED, OUTPUT);

  Serial.begin(9600);
  
  Serial.println(1);

  while (true) {
    digitalWrite(statusLED, HIGH);

    if (Serial.available() > 0) {
      int incoming = Serial.read();
      if (incoming == 1) {
        digitalWrite(statusLED, LOW);
        break;
      }
    }
    delay(100);
  }
}

void loop(){
  
}