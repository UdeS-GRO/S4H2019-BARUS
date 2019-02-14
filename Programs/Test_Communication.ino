
void setup() {
//Init of serial port
Serial.begin(9600);
pinMode(41, OUTPUT);
digitalWrite(41,LOW);
}

// Function for reading strings from Raspberry Pi
int read_Int() 
{
  int Byte1 = 0;
  int Byte2 = 0;
  if(Serial.available() > 0)
  {
    Byte1 = Serial.read();
    Byte2 = Serial.read(); 

    return ((Byte1<<8) + Byte2);
    
  }
  return -1;
 
}

// Function for reading strings from Raspberry Pi
String read_String() 
{
//String Temp = "";
String completeString = "Fail";
while (Serial.available()>0)
  {
    char receivedString = (char)Serial.read();
    //String completeString = Serial.readString();
    //char var = Serial.read();
    //Temp = String(var);
    completeString+= receivedString;
    
  }
  completeString+= '\n';
return completeString;
}

// Function for sending a string to RaspberryPi
void writeStrToRpi(String msg) 
{ 
 Serial.print(msg);
}

// Function for sending a string to RaspberryPi
void writeIntToRpi(int msg) 
{ 
 
 Serial.write(lowByte(msg));
 Serial.write(highByte(msg));
 
}


void loop()
{
  int message = read_Int();
  delay(500);
  writeIntToRpi(message);
  if (message == 5){
      digitalWrite(41, LOW);
      delay(500);
      digitalWrite(41, HIGH);
      delay(500);
      digitalWrite(41, LOW);
  }
  else {
    digitalWrite(41,LOW);
  }
  //String message;
  //message = read_String();
  //if (message.indexOf("allo") != -1) {
    //writeToRpi(message);
    //digitalWrite(41, LOW);
    //delay(500);
    //digitalWrite(41, HIGH);
    //delay(500);
    //digitalWrite(41, LOW)
}
 //else {
  // writeToRpi(message);
  //}

  //writeToRpi(message);
//}

