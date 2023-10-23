int count = 0;
String read;
String readed;
char buff[14];
void setup() {
  Serial.begin(19200);
  while(!Serial){}
}


//Dummy data to test:
//2. serial connection to Xbee
//2. Xbee script for processing and filtering
void loop() {
  delay(5000);
  count = 0;
  for (count; count < 10;){
    if (Serial.available()){
      //Short delay to ensure message isnt cut in half
      delay(50);
      //Fixed length of command message
      Serial.readBytes(buff, 14);
      if (buff[2] =='W'){
        Serial.println("junk_00.00_350_456_00.00_456_350_junk");
        delay(900);
        count++;
      }
      else{}
    }
    else{delay(10);}
    
  }
  for (int i=0; i < 8;){
    if (Serial.available()){
      //Short delay to ensure message isnt cut in half
      delay(50);
      //Fixed length of command message
      Serial.readBytes(buff, 14);

      if (buff[2] =="W"){
        Serial.println("junk_00.00_350_456_00.00_456_350_junk");
        i++;
      }
      else if(buff[2] == "A"){
        Serial.println(" 1_2_3_4_5_6_7");
        delay(800);
      }
    }
    else{delay(10);}
  }

}

