import subprocess

def configure(cmd):
    subprocess.Popen(cmd, shell=True).communicate()

if __name__ == '__main__':
    configure('chmod +x mget_setup.sh')
    configure('chmod +x mininet_setup.sh')
    configure('sudo ./mininet_setup.sh')
    configure('sudo ./mget_setup.sh')
    configure('sudo ./mininet_setup.sh') # Given in reproducing networks page to run this twice.
