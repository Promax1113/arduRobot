#include <DHT.h>
#include <ArduinoJson.h>

float duration, distance;

const int trigPin = 29;
const int echoPin = 28;

const int DHTPin = 2;

DHT dht(DHTPin, DHT22);

StaticJsonDocument<200> doc;

int get_distance(){
  
  // 0.0343 is sound vel in cm/microsecond
  
  digitalWrite(trigPin, LOW);  
	delayMicroseconds(2);  
	digitalWrite(trigPin, HIGH);  
	delayMicroseconds(10);  
	digitalWrite(trigPin, LOW);
  return (pulseIn(echoPin, HIGH) * .0343) / 2;    // divided by 2 to take into account just going or coming back, not whole time.
}


void setup() {
  pinMode(trigPin, OUTPUT);  
	pinMode(echoPin, INPUT);  
  pinMode(LED_BUILTIN, OUTPUT);


  Serial.begin(9600);
  Serial.println(100);
  unsigned long startTime = millis();
  while (millis() - startTime < 5000) {  // 5 second timeout
    if (Serial.available() > 0) {
      int data = Serial.read();
      if (data == 100) {
        digitalWrite(LED_BUILTIN, HIGH);  // Visual confirmation
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
            break;
          }
        }
      }


  dht.begin();

}

void loop(){
    doc.clear();
    doc["header"] = "data";
    doc["timestamp"] = millis();
    doc["distance"] = get_distance();
    doc["temperature"] = dht.readTemperature();
    doc["humidity"] = dht.readHumidity();
    serializeJson(doc, Serial);
    Serial.println();
    if (Serial.available()){
      char data = Serial.read();
    }
    delay(300);
}
