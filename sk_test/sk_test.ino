#include <ArduinoJson.h>
#include <DHT.h>


const int trigPin = 22;
const int echoPin = 23;
const int statusLED = 3;

const int testPin1 = 36;
const int testPin2 = 37;

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

  pinMode(testPin1, OUTPUT);
  pinMode(testPin2, OUTPUT);

  Serial.begin(9600);
  
  Serial.println(1);

  dht.begin();
  // wait for the DHT to start itself as it takes 55 microseconds
  delayMicroseconds(100);

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)){
    while (isnan(temperature) || isnan(humidity)){
      digitalWrite(statusLED, HIGH);
      delay(300);
      digitalWrite(statusLED, LOW);
      delay(300);
      temperature = dht.readTemperature();
      humidity = dht.readHumidity();
    }
  }

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
  float temperature;
  float humidity;
  float distance;

  doc.clear();
  doc["timestamp"] = millis();
  doc["distance"] = getDistance();
  doc["temperature"] = dht.readTemperature();
  doc["humidity"] = dht.readHumidity();

  serializeJson(doc, Serial);
  Serial.println();

  if (Serial.available() > 0){
    StaticJsonDocument<200> hostData;
    DeserializationError err = deserializeJson(hostData, Serial);

    if (err){
      return;
    }
    digitalWrite(testPin1, int(hostData["motor1"]));
    digitalWrite(testPin1, int(hostData["motor2"]));

  }
  delay(500);
}