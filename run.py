import subprocess

def configure(cmd):
    subprocess.Popen(cmd, shell=True).communicate()

if __name__ == '__main__':
    configure('sudo ./mget_setup.sh')
