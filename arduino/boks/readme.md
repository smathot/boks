Firmware
========

Flashing the Boks
-----------------

The `flash` script will automatically download the latest firmware from GitHub, insert the model name and number of buttons, and compile and upload the sketch to the Boks.

Upload latest firmware as model 'model_name' with 2 buttons:

	./flash	--model=model_name --buttons=2 --upload
	
Compile firmware from local file 'boks.ino.dist' and do not upload:

	./flash --src=boks.ino.dist
	
Show all options:

	./flash --help
	
Manually updating the Boks firmware
-----------------------------------

To manually update the Boks firmware (not recommended), please follow the instructions here:

- <http://osdoc.cogsci.nl/boks/source/>

Dependencies
------------

The `flash` script has been tested primarily on Ubuntu 12.04, although it should work on other systems as well, provided that all dependencies are installed. To install the dependencies that are not installed by default on Ubuntu 12.04, run the following commands:

	sudo apt-get install arduino-mk
