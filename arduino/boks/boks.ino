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

// The version and model are used to identify the box to the client. The
// version must be a 5 char string. The model musy be a 16 char string,
// optionally right-padded with whitespace for short mode names.
#define VERSION 			"0.1.6"
#define MODEL 				"dev.boks        "

// The respective pins on Arduino to which the buttons are connected
#define BUTTON_PIN_1 		8
#define BUTTON_PIN_2 		11
#define BUTTON_PIN_3 		9
#define BUTTON_PIN_4 		10
#define BUTTON_PIN_8		12 // Should be used for the photodiode
#define LED_PIN				13

// The baud rate for serial port communication
#define BAUD_RATE 			115200

// Signals for communicating with the library
#define CMD_RESET			1
#define CMD_IDENTIFY 		2
#define CMD_WAIT_PRESS 		3
#define CMD_WAIT_RELEASE 	4
#define CMD_WAIT_SLEEP		5
#define CMD_BUTTON_STATE	6
#define CMD_SET_T1			7
#define CMD_SET_T2			8
#define CMD_SET_TIMEOUT		9
#define CMD_SET_BUTTONS		10
#define CMD_SET_CONTINUOUS	11
#define CMD_GET_T1			12
#define CMD_GET_T2			13
#define CMD_GET_TD			14
#define CMD_GET_TIME		15
#define CMD_GET_TIMEOUT		16
#define	CMD_GET_BUTTONS		17
#define	CMD_LED_ON			18
#define CMD_LED_OFF			19

// In order to be able to communicate the timeStamp to the PC, it needs to be
// mapped onto an array
union timeStamp {
   unsigned long asLong;
   unsigned char asArray[4];
   char asChar[4];
};

// Define variables
int cmd;
int	fromState;
int toState;
int button1;
int button2;
int button3;
int button4;
int button8; // Photodiode
int	state1;
int state2;
int state3;
int state4;
int state8; // Photodiode
int pState1;
int pState2;
int pState3;
int pState4;
int pState8; // Photodiode
int i;
char continuous;
char c;
timeStamp t1;
timeStamp t2;
timeStamp ts;
timeStamp timeout;

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
	pinMode(BUTTON_PIN_8, INPUT); // Button 8 is the photodiode
	digitalWrite(BUTTON_PIN_8, HIGH);
	pinMode(LED_PIN, OUTPUT);	
	reset();
}

void reset()

	/**
	 * Reset Arduino to initial state
	 **/

{
	timeout.asLong = 0;
	t1.asLong = 0;
	t2.asLong = 0;	
	button1 = 1;
	button2 = 1;
	button3 = 1;
	button4 = 1;
	button8 = 0; // The photodiode is by default deactivated
	continuous = 0;
	digitalWrite(LED_PIN, HIGH); // Turn on LED
}

void loop()

	/**
	 * Start the main loop
	 **/

{
	cmd = Serial.read();
	if (cmd > 0) {

		if (cmd == CMD_RESET) {
			reset();

		} else if (cmd == CMD_IDENTIFY) {
			Serial.print(VERSION);
			Serial.print(MODEL);

		} else if (cmd == CMD_WAIT_PRESS || cmd == CMD_WAIT_RELEASE) {
			if (cmd == CMD_WAIT_PRESS) {
				fromState = HIGH;
				toState = LOW;
			} else {
				fromState = LOW;
				toState = HIGH;
			}			
			pState1 = -1;
			pState2 = -1;
			pState3 = -1;
			pState4 = -1;
			pState8 = -1;
			while (true) {
				t2.asLong = micros();
				if (timeout.asLong > 0 && t2.asLong - t1.asLong >=
					timeout.asLong) {
					Serial.write(255);
					break;
				}				
				state1 = digitalRead(BUTTON_PIN_1);
				state2 = digitalRead(BUTTON_PIN_2);
				state3 = digitalRead(BUTTON_PIN_3);
				state4 = digitalRead(BUTTON_PIN_4);				
				state8 = digitalRead(BUTTON_PIN_8);

				if (button1 && (continuous || pState1 == fromState)
					&& state1 == toState) {
					Serial.write(1);
					break;
				}
				if (button2 && (continuous || pState2 == fromState)
					&& state2 == toState) {
					Serial.write(2);
					break;
				}
				if (button3 && (continuous || pState3 == fromState)
					&& state3 == toState) {
					Serial.write(3);
					break;
				}
				if (button4 && (continuous || pState4 == fromState)
					&& state4 == toState) {
					Serial.write(4);
					break;
				}				
				if (button8 && (continuous || pState8 == fromState)
					&& state8 == toState) {
					Serial.write(8);
					break;
				}								
				pState1 = state1;
				pState2 = state2;
				pState3 = state3;
				pState4 = state4;
				pState8 = state8;
			}

		} else if (cmd == CMD_WAIT_SLEEP) {
			// Long delays cannot be handled on microsecond resolution
			if (timeout.asLong > 16383) {
				delay(timeout.asLong/1000);
			} else {
				delayMicroseconds(timeout.asLong);
			}

		} else if (cmd == CMD_BUTTON_STATE) {
			Serial.write(
				!digitalRead(BUTTON_PIN_1) |
				!digitalRead(BUTTON_PIN_2) << 1 |
				!digitalRead(BUTTON_PIN_3) << 2 |
				!digitalRead(BUTTON_PIN_4) << 3
			);

		} else if (cmd == CMD_SET_T1) {
			t1.asLong = micros();

		} else if (cmd == CMD_SET_T2) {
			t2.asLong = micros();

		} else if (cmd == CMD_SET_TIMEOUT) {
			Serial.readBytes(timeout.asChar, 4);

		} else if (cmd == CMD_SET_BUTTONS) {
			Serial.readBytes(&c, 1);
			if (c == 0) {
				// Do not allow the user to turn off all buttons!
				button1 = 1;
				button2 = 1;
				button3 = 1;
				button4 = 1;
				button8 = 0;
			} else {
 				button1 = c & 1;
 				button2 = (c >> 1) & 1;
 				button3 = (c >> 2) & 1;
 				button4 = (c >> 3) & 1;
				button8 = (c >> 7) & 1;
			}
		} else if (cmd == CMD_SET_CONTINUOUS) {
			Serial.readBytes(&continuous, 1);
l90 .
		} else if (cmd == CMD_GET_T1) {
			Serial.write(t1.asArray, 4);

		} else if (cmd == CMD_GET_T2) {
			Serial.write(t2.asArray, 4);

		} else if (cmd == CMD_GET_TD) {
			ts.asLong = t2.asLong - t1.asLong;
			Serial.write(ts.asArray, 4);

		} else if (cmd == CMD_GET_TIME) {
			ts.asLong = micros();
			Serial.write(ts.asArray, 4);

		} else if (cmd == CMD_GET_TIMEOUT) {
			Serial.write(timeout.asArray, 4);

		} else if (cmd == CMD_GET_BUTTONS) {
			Serial.write(button1 +
				(button2 << 1) |
				(button3 << 2) |
				(button4 << 3) |
				(button8 << 7));
					
		} else if (cmd == CMD_LED_ON) {
			digitalWrite(LED_PIN, HIGH);
			
		} else if (cmd == CMD_LED_OFF) {
			digitalWrite(LED_PIN, LOW);
		}
	}
}


