// This simple code allow you to send data from Arduino to Unity3D.

// uncomment "NATIVE_USB" if you're using ARM CPU (Arduino DUE, Arduino M0, ..)
//#define NATIVE_USB

// uncomment "SERIAL_USB" if you're using non ARM CPU (Arduino Uno, Arduino Mega, ..)
#define SERIAL_USB

long randNumber;
void setup() {
  #ifdef SERIAL_USB
    Serial.begin(250000); // You can choose any baudrate, just need to also change it in Unity.
    while (!Serial); // wait for Leonardo enumeration, others continue immediately
  #endif
}

// Run forever
void loop() {
  //sendData("Hello World!");
  int sensorValue = analogRead(A0);
  sendData(String(sensorValue));
  delay(1);
  // Choose your delay having in mind your ReadTimeout in Unity3D
}

void sendData(String data){
  #ifdef SERIAL_USB
    Serial.println(data); // need a end-line because wrmlh.csharp use readLine method to receive data
  #endif
}
