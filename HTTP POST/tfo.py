#!/usr/bin/python

import os
path = os.system('pwd')

from mininet.node import OVSController
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info, output
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import re


# Parsing the input arguments: bandwitdh, delay, name of site, tfo enabled/disabled

parser = ArgumentParser(description="Bufferbloat tests")

parser.add_argument('--bw-net', '-b',
                    type=float,
                    help="Bandwidth of bottleneck (network) link (Mb/s)",
                    required=True,
		    default=4)

parser.add_argument('--delay',
                    type=float,
                    help="Link propagation delay (ms)",
                    required=True)

parser.add_argument('--site',
		    type=str,
		    help="site name to be retrieved",
		    default="nyt")

parser.add_argument('--tfo',
                    type=bool,
                    help="enables tfo",
                    default=False)
# Expt parameters
args = parser.parse_args()

class TFOTopo(Topo):
    "Simple topology for bufferbloat experiment."

    def build(self, n=2):
        # Here I have created a switch.  If you change its name, its
        # interface names will change from s0-eth1 to newname-eth1.
        switch = self.addSwitch('s0')
        # We create two hosts and add links with appropriate
        # characteristics
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, h2, delay=(str(args.delay) + 'ms'), bw=args.bw_net)
        return

# Function to locally host the website on the host h1 passed in the argument with tfo enabled/disabled.
def start_webserver(net):
    h1 = net.get('h1')

    if (args.tfo == True):
      proc = h1.popen("python sites/webserver.py --tfo True", shell=True) # to run sub-process in mininet
    else:
      proc = h1.popen("python sites/webserver.py --tfo False", shell=True)
    sleep(5) #delay of 5 seconds
    return proc

#Here we load the webpage hosted by the host h1 using mget and time it to get the page load time for that website.
def measure_transfer_time(net):
    h1 = net.get('h1')
    h2 = net.get('h2')
    print h1.IP()
    print >> sys.stderr, "Working on retrieving from " + args.site
    client = h2.popen('time -f%%e curl --form "file=@/home/derikclive/TCP-Fast-Open-Experimentation/test_image.png" %s:80/' % (h1.IP()), shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = client.communicate()
    strtime = stderr.splitlines()[-1:]
    time = float(strtime[0])
    return time
#    return 0


def bufferbloat():
    topo = TFOTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, controller=OVSController)
    net.start()

    # This dumps the topology and how nodes are interconnected through links.
    # dumpNodeConnections(net.hosts)

    webserver = start_webserver(net)

    time_transfer = measure_transfer_time(net)

    print "    Time for transfer: %s" % (float(time_transfer)) + "\n"

    #webserver.kill()
    net.stop()
    # Ensure that all processes you create within Mininet are killed.
    # Sometimes they require manual killing.
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()

if __name__ == "__main__":
    bufferbloat()
