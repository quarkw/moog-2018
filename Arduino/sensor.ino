
const byte numChars = 32;
char receivedChars[numChars];
const byte numOutPins = 6;
int lastSent[numOutPins] = {0, 0, 0, 0, 0, 0};
int outputPins[numOutPins] = {3, 5, 6, 9, 10, 11};

boolean newData = false;
int pot = 0; //pot is short for Potentiator

void setup() {
    Serial.begin(9600); //set Baud
}

void loop() {


//    getPotData();
//    potProcessor();
    sendDataToComputer();
    recvWithStartEndMarkers();
    showNewData();

   
}

void getPotData() {
  Serial.println(analogRead(pot));
}

void potProcessor() {
  int val = analogRead(pot); //reads input $pot (somewhere on the softPot)
  analogWrite(3, val/4); //write to analog IN port 3
  Serial.print("VAL: " );
  Serial.print(val/4);
  Serial.print("\n");

}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = 2;
    char endMarker = 3;
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    static byte ndx = 0;
    if (newData == true) {
//        Serial.print("This just in ... ");
        if(String(receivedChars).length() == 6){
//          Serial.println("ok");
          sendDataToMoog();
        } else {
//            for(int i=0; i < numOutPins; i++){
//                analogWrite(outputPins[i], lastSent[i]);
//            } 
        }
//        Serial.println("sad");
//        Serial.print(String(receivedChars).length());
//        Serial.println(receivedChars);
        newData = false;
    }
}

void sendDataToComputer() {
  while(!Serial.available()) { //wait for data
//  while(Serial.available()) {
      int val = analogRead(pot); //init pot var
//      analogWrite(3, val/4); //write to analog IN port 3
      Serial.println(val);
//      Serial.write(val/4);

      Serial.flush();
  }
}

int softPot = 0;
int myoX = 0;
int myoY = 0;
int myoZ = 0;

void sendDataToMoog() {
//  softPot = analogRead();
  for(int i=0; i < numOutPins; i++){
    if((int) receivedChars[i] > 4){
      analogWrite(outputPins[i], receivedChars[i]);
      lastSent[i] = receivedChars[i];
    }
  }
//  analogWrite(10, ); //emotion
//  analogWrite(11, ); //emotion?
}

