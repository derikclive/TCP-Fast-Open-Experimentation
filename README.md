# TCP-Fast-Open-Experimentation
## Course Code: CO300
## Assignment

### Webpage

https://derikclive.github.io/TCP-Fast-Open-Experimentation/

### Overview
TCP Fast Open (TFO) is an experimental update to TCP that enables data to be
exchanged safely during TCP's connection handshake. It does so to save one RTT, while
avoiding severe security threats. The summary of the TCP Fast Open RFC can he found [here](https://github.com/derikclive/TCP-Fast-Open-Experimentation/wiki/RFC-7413---TFO-Summary).

### Why TCP Fast Open when we have persistent HTTP Connections?
HTTP Persistent Connections reuses TCP connections for multiple transactions ad thus saved the overhead involved in the three way handshake. However accoring to the statistics from Chrome, over one third of the HTTP requests (cold requests) make use of new TCP connections. But TFO overcomes this issue by allowing data to be exchanged during the initial TCP handshake itself.

### To run this code, set up a Google Cloud Instance with the folowing specs:

#### Machine Type

* 1 vCPU with 3.75 GB memory

#### Boot Disk

* Ubuntu 14.04 LTS

#### Check the following under Firewall

* Allow HTTP Traffic
* Allow HTTPS Traffic

Click ‘Create’.

Run the following commands after logging in through SSH:
```
sudo apt-get update
sudo apt-get -y install git
```

Clone the repository
```
git clone https://github.com/derikclive/TCP-Fast-Open-Experimentation/
```

You can check the perfomance of TFO for the following two HTTP request methods:

1. HTTP GET

  To see the results of the GET request using TFO do the following:

  * Run the python file to start:
 
```
cd TCP-Fast-Open-Experimentation/HTTP\ GET
sudo python run.py
```

  * After 15-30 minutes, the results are written into results.txt and the file plots.png will display the comparison of TFO and Vanilla TCP using graphs.

2. HTTP POST

  To see the results of the POST request using TFO do the following:

  * Upload the file you want to upload to the server into the TCP-Fast-Open-Experimentation folder.
  
```
cd TCP-Fast-Open-Experimentation/HTTP\ POST
```
  
  * Change the path in the measure_transfer_time function of the tfo.py file to point to the path of the file you uploaded.
  
  * Run the python file to start:
  
```
sudo python run.py
```
  * After 15-30 minutes, the results are written into results.txt and the file plots.png will display the compaarison of TFO and Vanilla TCP using graphs.
  

### Challenges Faced

* openvswitch-controller isn't supported on Ubuntu 16.04 and we couldn't deploy mininet on our machines. Our project had to be completely moved to the cloud. 
* The documentation for the CS244'17 TFO project was very minimal.
* The project initially used SimpleHTTPServer which does not support POST requests.It only supports GET requests. We used BaseHTTPServer (which is the base class for SimpleHTTPServer) instead and wrote POST and GET handling requests from scratch.
* There was some difficulty in using the curl command (for POST requests) on mininet. On changing the IP address of the hosted website we got the curl command to work properly on mininet.

### Inferences

* From our experiments we found that TCP Fast Open was especially useful for website visitors who are a great distance away from the origin server therefore increasing round trip times.
* We also observed that the page load time (HTTP GET requests) of TFO over Vanilla TCP improved as the size of the webpage increased and as the bandwidth increases.
* But there was no improvement on using TFO when a HTTP POST request (Uploading a file) was given to the the server.
* We also observed that our PLTs are significantly larger than the ones in the paper for amazon.com. We believe that this is reasonable given that the paper was published in 2011, and the sites mentioned likely had much slimmer pages. 

### Enabling TFO in linux kernel

You need to have linux kernel at least 3.7.

You can check via `uname -r`, it will give the result similar to following.

``4.4.0-98-generic``

Then follow the following steps to enable Fast TCP Open

Edit `/etc/sysctl.conf` and add the following line to its end of file
   `net.ipv4.tcp_fastopen = 3`
   
Save the file.

Execute `sysctl -p` to make it taken into effect.

Make it permanent even after rebooting system by adding the following line into `/etc/rc.local` 

   `echo 3 > /proc/sys/net/ipv4/tcp_fastopen`
   
To view TCP connections and to view the TFO cookies generated, use

`ip tcp_metrics`


### References
[1] Sivasankar Radhakrishnan, Yuchung Cheng, Jerry Chu, Arvind Jain, and Barath Raghavan. 2011. TCP fast open. In Proceedings of the Seventh COnference on emerging Networking EXperiments and Technologies (CoNEXT '11). ACM, New York, NY, USA, , Article 21 , 12 pages. DOI=http://dx.doi.org/10.1145/2079296.2079317.

[2] https://tools.ietf.org/html/rfc7413.

[3] https://reproducingnetworkresearch.wordpress.com/2016/05/30/cs244-16-tcp-fast-open/.

[4] https://reproducingnetworkresearch.wordpress.com/2017/06/05/cs244-17-tcp-fast-open/.

