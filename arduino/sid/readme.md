Serial ID
=========

Writing a serial ID
-------------------

The `flash` script will write a serial ID to the eeprom of the Arduino. The serial ID must a six character string.

	./flash	--sid=AB1234 --upload
	
This will erase the firmware on the Arduino! After writing a serial ID, you will need to reflash the Boks firmware.
		
Dependencies
------------

The `flash` script has been tested primarily on Ubuntu 12.04, although it should work on other systems as well, provided that all dependencies are installed. To install the dependencies that are not installed by default on Ubuntu 12.04, run the following commands:

	sudo apt-get install arduino-mk
	

