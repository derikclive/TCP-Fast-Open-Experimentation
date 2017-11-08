Go to Google Cloud Engine and click ‘CREATE INSTANCE’. The instance should have the following properties:
 
Machine Type
1 vCPU with 3.75 GB memory
 
Boot Disk
Ubuntu 14.04 LTS
 
Check the following under Firewall
Allow HTTP Traffic
Allow HTTPS Traffic
 
Click ‘Create’
 
Next, you will want to SSH into the instance. Once you have done so, run the following commands:
 
sudo apt-get update
sudo apt-get -y install git
 
cd ~; git clone https://logicalmath333@bitbucket.org/cs240groupproject/project3.git
 
Then, set up your git information like the following:
 
cd project3; sudo python run.py
 
Wait 15-30 minutes
 
Check out the results in results.txt

