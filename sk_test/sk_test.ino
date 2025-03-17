void setup() {
  Serial.begin(9600);
  Serial.println(100);


}

void loop() {
  if (Serial.available() > 0){
    String data = Serial.readString();
    Serial.println(data.c_str());

  }

}
