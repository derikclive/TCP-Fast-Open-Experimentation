#sudo mount -t tmpfs cgroup_root /sys/fs/cgroup
#mkdir /sys/fs/cgroup/cpuset
#sudo mount -t cgroup cpuset -o cpuset /sys/fs/cgroup/cpuset/
#sudo apt-get -y install cgroup-bin

sudo rm -rf /usr/local/bin/mn /usr/local/bin/mnexec \
    /usr/local/lib/python*/*/*mininet* \
    /usr/local/bin/ovs-* /usr/local/sbin/ovs-*
cd ~
git clone git://github.com/mininet/mininet
sudo apt-get -y install help2man
sudo apt-get -y install python-setuptools

sudo apt-get -y install mininet
sudo service openvswitch-controller stop
sudo update-rc.d openvswitch-controller disable

sudo dpkg-reconfigure openvswitch-datapath-dkms
sudo service openflow-switch restart

sudo mn -c

sudo apt-get -y install make
cd ~/mininet
sudo git fetch
sudo git checkout master   # Or a specific version like 2.2.1
sudo git pull
sudo make install

sudo mn -c
sudo service openvswitch-controller stop
sudo update-rc.d openvswitch-controller disable
