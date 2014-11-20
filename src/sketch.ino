//This is the code to make the arduino function as an ohmmeter
/*-----( Import needed libraries )-----*/
#include "OneWire.h"
#include "DallasTemperature.h"

#define ONE_WIRE_BUS 3 /*-(Connect to Pin 2 )-*/
OneWire ourWire(ONE_WIRE_BUS);
DallasTemperature sensors(&ourWire);

volatile int bcount=0;
void setup() {
  Serial.begin(115200);
  attachInterrupt(0, bubble, CHANGE);
  sensors.begin();
}

void loop() {
	temp();
	Serial.print(" ");
	light();
	Serial.print(" ");
	bubbles();
	Serial.println("");
	delay(10000);
}
void temp() {
  sensors.requestTemperatures();
  Serial.print("celsius:");
  Serial.print(sensors.getTempCByIndex(0));
}

void light() {
	int analogPin= 1;
	float raw= 0;
	int Vin= 5;
	float Vout= 0;
	float buffer= 0;
	float avg = 0;
	for(int i =0; i<200; i++) {
		avg += analogRead(analogPin);
	}
	raw = avg/200; 
	buffer= raw * Vin;
	Vout= (buffer)/1023.0;
	Serial.print("lux:");
	Serial.print(Vout*1333);
}

void bubbles() {
	int bubblecount=0;
	if(bcount>=8) {
		bubblecount+=bcount/8;
		bcount=0;
	}
	Serial.print("bubbles:");
	Serial.print(bubblecount);
}

void bubble() {
  bcount++;
}
