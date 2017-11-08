#!/usr/bin/python

import sys
import re

vanilla_times = []
tfo_times = []
site = None;
tcp_protocol = None;
tfo = None;
filename = "results.txt"

with open(filename) as f:
	for line in f:
		if "===" in line:
			line = line.replace("=", "")
			line = line.replace(" ", "")
			site = line.strip()
		if "cubic" in line:
			tcp_protocol = "cubic"
		if "westwood" in line:
			tcp_protocol = "westwood"
		if "tfo enabled" in line:
			tfo = True
		if "vanilla tcp" in line:
			tfo = False
		if "Delay" in line:
			m = re.search("\d", line)
			first_digit = m.start()
			delay = line[first_digit:]
			delay = delay.strip()

		if "Bandwidth" in line:
			m = re.search("\d", line)
			first_digit = m.start()
			band = line[first_digit:]
			band = band.strip()

		if "Time for transfer" in line:
			m = re.search("\d", line)
			first_digit = m.start()
			time = float(line[first_digit:])
			if tfo:
				tfo_times.append(time)
			else:
				vanilla_times.append(time)


			if delay == "200" and tfo and band == "10":
				print len(vanilla_times), len(tfo_times)
				print "\nsite: " + site
				print "tcp protocol: " + tcp_protocol
				delays = [20]
				bandwidths = [1, 2]
				m = len(delays)
				n = len(bandwidths)
				for i in range(len(delays)):
					for j in range(len(bandwidths)):
						print "delay: " + str(delays[i])
						print "bandwitdh: " + str(bandwidths[j])
						print "% improvement: " + str(100 * (abs(tfo_times[i*n+j] - vanilla_times[i*n+j]) / (vanilla_times[i*n+j])))
				vanilla_times = []
				tfo_times = []
