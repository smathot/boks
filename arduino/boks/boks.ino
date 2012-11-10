/**
 * This file is part of boks.
 * 
 * boks is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * boks is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with boks. If not, see <http://www.gnu.org/licenses/>.
 **/

// The version and model are used to identify the box to the client
#define VERSION 			"0.1.2" 			// Must be 5 chars
#define MODEL 				"test.boks       " // Must be 16 chars

// The respective pins on Arduino to which the buttons are connected
#define BUTTON_PIN_1 		2
#define BUTTON_PIN_2 		4
#define BUTTON_PIN_3 		7
#define BUTTON_PIN_4 		8

// The minimum number of consecutive samples required to detect a button
// press or release
#define DEBOUNCE_COUNT 		100

// The baud rate for serial port communication
#define BAUD_RATE 			115200

// Signals for communicating with the library
#define CMD_IDENTIFY 		1
#define CMD_WAIT_PRESS 		2
#define CMD_WAIT_RELEASE 	3
#define CMD_GET_STATE 		4
#define CMD_GET_TIME_NOW 	5
#define CMD_GET_TIME_EVENT 6
#define CMD_SET_BUTTONS 	7
#define CMD_SET_TIMEOUT 	8

// In order to be able to send the timeStamp, it needs to be mapped onto an array
union timeStamp {
   unsigned long asLong;
   unsigned char asArray[4];
};

// Define variables
int cmd;
int fromState;
int toState;
int state;
int state1;
int pState1;
int state2;
int pState2;
int state3;
int pState3;
int state4;
int pState4;
int count;
timeStamp ts;

void setup()

	/** 
	 * Setup the buttons as input
	 **/

{
	Serial.begin(BAUD_RATE);
	pinMode(BUTTON_PIN_1, INPUT);
	digitalWrite(BUTTON_PIN_1, HIGH);
	pinMode(BUTTON_PIN_2, INPUT);
	digitalWrite(BUTTON_PIN_2, HIGH);  
	pinMode(BUTTON_PIN_3, INPUT);
	digitalWrite(BUTTON_PIN_3, HIGH);
	pinMode(BUTTON_PIN_4, INPUT);
	digitalWrite(BUTTON_PIN_4, HIGH);    
}

boolean debounceLoop(int buttonPin, int buttonNr) {
	
	/**
	 * Repeatedly samples a given pin, and sends a buttonNr if sufficient
	 * consecutive samples have been collected.
	 * 
	 * Arguments:
	 * int buttonPin	-- the pin to samples
	 * int buttonNr 	-- the nr of the button to send in case a signal has been
	 * 					   detected
	 * 
	 * Returns:
	 * true or false, depending on whether a sample has been detected
	 **/
	
	// Debounce loop. We need to receive a minimum number of
	// samples to determine that the button is actually
	// pressed.
	count = 0;
	while (true) {
		state = digitalRead(buttonPin);
		if (state != toState) {
			return false; // Debounce failed							
		}						
		if (count++ == DEBOUNCE_COUNT) {
			Serial.write(buttonNr);
			return true;
		}
	}
return false;
}

void loop()

	/**
	 * Start the main loop
	 **/

{
	cmd = Serial.read();
	if (cmd > 0) {
		
		if (cmd == CMD_WAIT_PRESS || cmd == CMD_WAIT_RELEASE) {						
			
			// If the boks gets a command to wait for a press or a release it
			// simply waits until a key is pressed or released and sends a signal
			// byte to the requester.
			
			// The transition of interest depends on whether we are interested
			// in a press or a release.
			if (cmd == CMD_WAIT_PRESS) {
				fromState = HIGH;
				toState = LOW;				
			} else {
				fromState = LOW;
				toState = HIGH;
			}
			
			pState1 = -1;
			
			// Poll for button presses/ releases until an event has been
			// detected.
			while (true) {
				ts.asLong = micros();
				state1 = digitalRead(BUTTON_PIN_1);				
				state2 = digitalRead(BUTTON_PIN_2);
				state3 = digitalRead(BUTTON_PIN_3);
				state4 = digitalRead(BUTTON_PIN_4);
				if (pState1 == fromState && state1 == toState) {
					if (debounceLoop(BUTTON_PIN_1, 1)) {
						break;
					}
				}
				if (pState2 == fromState && state2 == toState) {
					if (debounceLoop(BUTTON_PIN_2, 2)) {
						break;
					}
				}
				if (pState3 == fromState && state3 == toState) {
					if (debounceLoop(BUTTON_PIN_3, 3)) {
						break;
					}
				}
				if (pState4 == fromState && state4 == toState) {
					if (debounceLoop(BUTTON_PIN_4, 4)) {
						break;
					}
				}				
				pState1 = state1;
				pState2 = state2;
				pState3 = state3;
				pState4 = state4;
			}
			
		} else if (cmd == CMD_GET_STATE) {	
			
			// If the boks gets a command to return the button state, it
			// immediately responds by sending a byte where the active buttons
			// are 1, and the inactive buttons are 0.		
			
			Serial.write(
				!digitalRead(BUTTON_PIN_1) |
				!digitalRead(BUTTON_PIN_2) << 1 |
				!digitalRead(BUTTON_PIN_3) << 2 |
				!digitalRead(BUTTON_PIN_4) << 3				
			);		
			
		} else if (cmd == CMD_GET_TIME_NOW || cmd == CMD_GET_TIME_EVENT) {
			
			// If the boks gets a command to return the time, it optionally gets
			// the current time (if CMD_GET_TIME_NOW) and then sends it as an
			// unsigned long to the requester.
			
			if (cmd == CMD_GET_TIME_NOW) {
				ts.asLong = micros();
			}
			Serial.write(ts.asArray, 4);
			
		} else if (cmd == CMD_IDENTIFY) {
			
			// If the boks gets a command to identify itself, it sends a 
			
			Serial.print(VERSION);
			Serial.print(MODEL);
		}
	}
}


