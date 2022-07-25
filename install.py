#!/usr/bin/env python3

import subprocess as sub
import os
import sys

red = "\033[0;31m"
green = '\033[0;32m'

def control_uid():
    if os.getuid() != 0:
        print(f"{red}USER ROOT")
        sys.exit(0)

def install():
    print(f"{green} INSTALLING")
    sub.run(["sudo","pip3","install","alive-progress"],capture_output=True)

    from alive_progress import alive_bar 
    import time 

    total = 100
    with alive_bar(total) as bar:
        for _ in range(100):
            time.sleep(.5)

            if _ == 10:
                
                sub.run(["sudo","python3","-m","pip","install","scapy"],capture_output=True)
            elif _==20:
               
                sub.run(["sudo","python3","-m","pip","install","nmap"],capture_output=True)

            elif _==30:

                 sub.run(["chmod","+x","main.py"],capture_output=True)

            elif _==50:
               
                sub.run(["sudo","python3","-m","pip","install","netfilterqueue"],capture_output=True)

            bar()

control_uid()
install()