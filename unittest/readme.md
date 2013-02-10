Boks test suite
===============

Usage
-----

To run individual tests, run:

	./unittest [buttons] [led] [photodiode] [latency] [commspeed] [noise]
	
To run the full test suite run:

	./testreport
	
This will generate a test report in three formats:

	testreport.md
	testreport.html
	tesrreport.pdf
	
Dependencies
------------

This test suite has been tested primarily on Ubuntu 12.04, although it should work on other systems as well, provided that all dependencies are installed. To install the dependencies that are not installed by default on Ubuntu 12.04, run the following commands:

	sudo add-apt-repository ppa:smathot/cogscinl
	sudo apt-get update
	sudo apt-get install opensesame expyriment kramdown wkhtmltopdf rubygems
	sudo gem install kramdown
	