import subprocess
import os

class CfgSetter():

    def __init__(self):
        return 0

    @staticmethod
    def turn_on_tfo():
        #sysctl is a tool for examining and changing the kernel parametes during the run time.
        intval = int(0x207)
        return configure('sudo sysctl net.ipv4.tcp_fastopen=' + str(intval))

    @staticmethod
    def turn_off_TFO():
        return configure('sudo sysctl net.ipv4.tcp_fastopen=0')
