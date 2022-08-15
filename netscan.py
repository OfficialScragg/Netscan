#!/usr/bin/env python3

import threading, socket, progressbar

# Settings
base_ip = '139.162.248.'
ip_range = range(1, 255)
ports = [20, 21, 22, 23, 25, 53, 80,110, 119, 123, 143, 161, 194, 443] # common ports
out = open('scan-res.txt', 'w')

# Variables
open_threads = 0
widgets = [ 'Scanning...', progressbar.Bar('#') ]
bar = progressbar.ProgressBar(widgets=widgets).start()

def scan(ip, ports):
    global open_threads, out, bar
    res = ip+" -> "
    for p in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            conn = s.connect_ex((ip, p))
            if(conn == 0) :
                if res == ip+" -> ":
                    res = res + str(p)
                else:
                    res = res + "," + str(p)
            s.close()
    out.write(res+"\n")
    open_threads-=1
    bar.update(((len(ip_range)-open_threads)/len(ip_range))*100)
    if(open_threads == 0):
        bar.update(100)
        print()

def setup():
    global open_threads
    threads = []
    for ip in ip_range:
        threads.append(threading.Thread(target=scan, args=(str(base_ip+str(ip)), ports,)))
    for t in threads:
        t.start()
        open_threads+=1
    
if __name__ == '__main__':
    setup()