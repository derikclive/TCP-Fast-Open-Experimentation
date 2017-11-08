#!/bin/bash

# Note: Mininet must be run as root.  So invoke this shell script
# using sudo.

# Units are in Mbps
# https://github.com/mininet/mininet/wiki/Introduction-to-Mininet
bwnet=4
touch results.txt
rm results.txt

for site in nyt amazon wiki_tcp wsj; do
  echo -n "====== " >> results.txt
  echo -n $site >> results.txt
  echo " ======" >> results.txt
  echo -n "  " >> results.txt
  echo cubic >> results.txt
  echo cubic > /proc/sys/net/ipv4/tcp_congestion_control
  for tfo in 0 519; do
    if [ "$tfo" = "0" ]; then
      echo "  vanilla tcp" >> results.txt
    else
      echo "  tfo enabled" >> results.txt
    fi
    for delay in 20 100 200; do
      echo -n "    Delay (ms): " >> results.txt
      echo $delay >> results.txt
      echo $tfo > /proc/sys/net/ipv4/tcp_fastopen
      if [ "$tfo" = "0" ]; then
        python tfo.py -b $bwnet --delay $delay --site $site >> results.txt
      else
        python tfo.py -b $bwnet --delay $delay --site $site --tfo True >> results.txt
      fi
    done
  done
done

echo "IMPROVMENT" >> results.txt
echo "=================================" >> results.txt
python results_parser.py results.txt >> results.txt
