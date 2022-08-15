#!/usr/bin/env python3

import threading
import socket

# Settings
base_ip = '139.162.248.'
ip_range = range(130, 150)
ports = range(19, 30)
out = open('scan-res.txt', 'w')

# Variables
open_threads = 0

def scan(ip, ports):
    global open_threads, out
    res = ip+" -> "
    print ('Scanning: ', ip)
    for p in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            conn = s.connect_ex((ip, p))
            if(conn == 0) :
                print(str(ip)+':%d -> OPEN' % (p,))
                if res == ip+" -> ":
                    res = res + str(p)
                else:
                    res = res + "," + str(p)
            s.close()
    print(ip, "scanned!")
    out.write(res+"\n")
    open_threads-=1
    if(open_threads == 0):
        print("---- Done ----")

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