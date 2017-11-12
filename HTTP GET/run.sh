#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

# Units are in Mbps
# https://github.com/mininet/mininet/wiki/Introduction-to-Mininet
#bwnet=4
touch results.txt
rm results.txt

for site in flipkart amazon_in myntra jabong wiki_tcp google youtube ; do
  echo -n "====== " >> results.txt
  echo -n $site >> results.txt
  echo " ======" >> results.txt
  echo -n "  " >> results.txt

  # Using the cubic function for the size of the congestion window.
  # You can also use the westwood and reno tcp congestion algorithms.

  echo cubic >> results.txt
  echo cubic > /proc/sys/net/ipv4/tcp_congestion_control

  # Using mget to retive data from the hosted website using mget with,

  # i) tfo enabled: code 519 (519 = 0x200 OR 0x1 OR 0x2 OR 0x4 )
      # where these flags stand for
    	#   0x1: (client) enables sending data in the opening SYN on the client.
    	#   0x2: (server) enables the server support, i.e., allowing data in
    	# 		a SYN packet to be accepted and passed to the
    	# 		application before 3-way handshake finishes.
    	#   0x4: (client) send data in the opening SYN regardless of cookie
    	# 		availability and without a cookie option.
    	# 0x200: (server) accept data-in-SYN w/o any cookie option present.
    	# 0x400: (server) enable all listeners to support Fast Open by
    	# 		default without explicit TCP_FASTOPEN socket option.

  # ii) tfo disabled: code 0


  for tfo in 0 519; do
    if [ "$tfo" = "0" ]; then
      echo "  vanilla tcp" >> results.txt
    else
      echo "  tfo enabled" >> results.txt
    fi
    for delay in 20 100 200; do
      echo -n "    Delay (ms): " >> results.txt
      echo $delay >> results.txt

      for bwnet in 1 2 5 10; do
        echo -n "    Bandwidth (Mbps): " >> results.txt
        echo $bwnet >> results.txt
        # manually configuring the tcp fast open by changing the flag in /proc/sys/net/ipv4/tcp_fastopen
        # this can also be done by using sysctl


        echo $tfo > /proc/sys/net/ipv4/tcp_fastopen

        if [ "$tfo" = "0" ]; then
          python tfo.py -b $bwnet --delay $delay --site $site >> results.txt
        else
          python tfo.py -b $bwnet --delay $delay --site $site --tfo True >> results.txt
        fi
      done
    done
  done
done

echo "IMPROVMENT" >> results.txt
echo "=================================" >> results.txt
python results_parser.py results.txt >> results.txt
python plotter.py
