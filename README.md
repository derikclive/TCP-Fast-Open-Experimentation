# TCP-Fast-Open-Experimentation
## Course Code: CO300
## Assignment

### Overview
TCP Fast Open (TFO) is an experimental update to TCP that enables data to be
exchanged safely during TCP's connection handshake. It does so to save one RTT, while
avoiding severe security threats.

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

Run the python file to start:
```
cd TCP-Fast-Open-Experimentation
sudo python run.py
```

After 15-30 minutes, the results are written into results.txt

### Challenges Faced

* We faced a lot of issuses when we tried to install mininet on Ubuntu 16.04 (openvswitch-controller), so we had to switch to Ubuntu 14.04.
* We also took a lot of time to understand the code of the CS244'17 TFO project as it wasn't well documented.

### References
[1] Sivasankar Radhakrishnan, Yuchung Cheng, Jerry Chu, Arvind Jain, and Barath Raghavan. 2011. TCP fast open. In Proceedings of the Seventh COnference on emerging Networking EXperiments and Technologies (CoNEXT '11). ACM, New York, NY, USA, , Article 21 , 12 pages. DOI=http://dx.doi.org/10.1145/2079296.2079317.

[2] https://tools.ietf.org/html/rfc7413.

[3] https://reproducingnetworkresearch.wordpress.com/2016/05/30/cs244-16-tcp-fast-open/.

[4] https://reproducingnetworkresearch.wordpress.com/2017/06/05/cs244-17-tcp-fast-open/.
