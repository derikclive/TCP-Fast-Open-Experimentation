# TCP-Fast-Open-Experimentation

## Course Code: CO300

## Assignment

### Overview

There are four main files for a high level understanding that perform the whole task of TFO experimentation namely

* run.py

* run.sh

* tfo.py

* webserver.py

### Detailed flow of the code

1)	Details of "run.py" file 

	The execution starts of at the "run.py" file.

   	This file sets up mininet (by calling "mininet_setup.sh"), mget ("by calling mget_setup.sh") and makes a 

   	call to run the file "run.sh".

2)	Details of "run.sh" file

	* Iterates thrugh the various sites that have been previously downloaded for testing purposes.

		* Adds the cubic function to the tcp_congestion_control file in kernel

		* Sets the TFO flag in the tcp_fastopen file in the kernel

		Performs experiment for both vanilla TCP and TFO

		* If TCP run the "tfo.py" file.

		* If TFO run the "tfo.py" file with additional argument "--tfo True".

		* Add results obtained by both the above in "results.txt" file.

3)	Details of the "tfo.py" file

	In this file the main experiment is carried out for a given site.

	* Defines and accepts all the arguments required like bandwitdh, delay, name of site, tfo enabled/disabled.

	* The "TFOTopo" function basically sets up the network in mininet with one switch(s0) and two hosts(h1,h2 

	  which will communicate with each other) 

	* The "start_webserver" function does the task of making h1 a web server in mininet by passing control to

	  "webserver.py"

	* The "measure_transfer_time" function measures the time taken for the mget request from the mininet

	  client to server. 
	
	* The "bufferbloat" function acts as the driver in this file and makes calls to the previously mentioned 

	  functions in the file i.e setting up mininet network and server.


	All these results are then returned to "run.sh" file which then prints all the results obtained into a 

	file namely the "results.txt" file.

4) 	Details of the "webserver.py" file

	Creates the BaseHttpServer with functions handling the GET and POST requests using the CO303Handler and also sets the port number to serve on.

### Analysis of results

This is handled by two files:

* results_parser.py

* Plot.ipynb

1)	Details of the "results_parser.py" file:

	* It reads from "results.txt" (which is written into by "run.sh").

	* Calculation of improvement is done and appended into "results.txt".

	* The data read from "results.txt" is parsed and then converted into a csv file ("results.csv").

2)	Details of the "Plot.ipynb" file:

	* An IPYNB file is a notebook document used by Jupyter Notebook, an interactive computational environment designed to help scientists work with the Python language and their data.

	* The data from "results.csv" is used to plot the charts.

	* Pandas is used to read and store the data from the CSV file.

	* Matplotlib is used to plot the data.

	* Bar graphs for each website at different bandwidth  is shown to display difference in performance between Vanilla TCP and TCP Fast Open.





