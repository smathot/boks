Flashing the Boks
=================

The `flash` script will automatically download the latest firmware from GitHub, insert the model name and number of buttons, and compile and upload the sketch to the Boks.

Upload latest firmware as model 'model_name' with 2 buttons:

	./flash	--model=model_name --buttons=2 --upload
	
Compile firmware from local file 'boks.ino' and do not upload:

	./flash --src=boks.ino
	
Show all options:

	./flash --help

