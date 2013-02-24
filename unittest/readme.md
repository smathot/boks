Boks test suite
===============

Usage
-----

To run individual tests, run:

	./unittest [N] [width] [height] [backends] [buttons|led|photodiode|latency|commspeed|noise]
	
For example, the following command will run the photodiode test 10 times on a 1280x1024 resolution with all three back-ends.
	
	./unittest 10 1280 1024 psycho,xpyriment,legacy photodiode
	
To run the full test suite run:

	./testreport [N] [width] [height] psycho,xpyriment,legacy
	
For example, the following command will run the full suite with 100 measurements per test on a 1024x768 resolution:

	./testreport 100 1024 768 psycho,xpyriment,legacy 
	
This will generate a test report in three formats:

	testreport.md
	testreport.html
	testreport.pdf
	
Dependencies
------------

This test suite has been tested primarily on Ubuntu 12.04, although it should work on other systems as well, provided that all dependencies are installed. To install the dependencies that are not installed by default on Ubuntu 12.04, run the following commands:

	sudo add-apt-repository ppa:smathot/cogscinl
	sudo apt-get update
	sudo apt-get install opensesame expyriment wkhtmltopdf rubygems
	sudo gem install kramdown
	
