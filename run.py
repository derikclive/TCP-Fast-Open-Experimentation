import subprocess

def configure(cmd):
    subprocess.Popen(cmd, shell=True).communicate()

if __name__ == '__main__':
   
    subprocess.call(["chmod", "+x" , "mget_setup.sh"])
    configure("sudo ./mget_setup.sh")

    configure('chmod +x mininet_setup.sh')
 
    configure('sudo ./mget_setup.sh')
    configure('sudo ./mininet_setup.sh') # Given in reproducing networks page to run this twice.

    subprocess.call(["chmod", "+x" , "download.sh"])
    configure(' sudo /bin/bash download.sh')
