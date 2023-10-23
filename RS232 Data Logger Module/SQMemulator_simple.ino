int count = 0;
String read;
String readed;
char buff[0];
void setup() {
  Serial.begin(19200);
  while(!Serial){}
}


//Dummy data to test:
//2. serial connection to Xbee
//2. Xbee script for processing and filtering
void loop() {
  delay(5000);

  for (int i=0; i < 10; i++){
    Serial.println(" B_0_1_0_3_2");
    delay(1000);
  }
  for (int i=0; i < 8; i++){
    Serial.println(" B_1_2_3_4_2");
    delay(1000);
  }
  Serial.println(" B_end");

}

