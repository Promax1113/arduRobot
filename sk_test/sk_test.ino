float duration, distance;

const int trigPin = 2;
const int echoPin = 3;

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

  Serial.begin(9600);
  Serial.println(100);


}

void loop() {
  if (Serial.available() > 0){
    Serial.println(get_distance());
    delay(100);

      
  }

}
