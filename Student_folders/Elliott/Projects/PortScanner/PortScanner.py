import socket
import threading
import argparse
import itertools
import pyping
import subprocess
import os
import time
from Queue import Queue

lock        = threading.Lock()
_start      = time.time()
pingQueue   = Queue()
portQueue   = Queue()
hostQueue   = Queue()
openPorts   = {}

def pingTarget(address, sPort, ePort,  delay, output):
    with open(os.devnull, "wb") as limbo:
        result=subprocess.Popen(["ping", "-c", "1", "-w", ".05", address],stdout=limbo, stderr=limbo).wait()
        with lock:                    
            if not result:
                print "Ping: (Active)", address
                output.append(address)
                return True
            else:
                return False

def pingThreader(sPort, ePort,  delay, output):
    while True:
        worker=pingQueue.get()
        pingTarget(worker, sPort, ePort,  delay, output)
        pingQueue.task_done()

def portThreader(address, i, delay, tempQueue, proto, outTcp, outUdp):
    while True:
        worker=tempQueue.get()
        connectSocket(address, worker, delay, proto, outTcp, outUdp)
        tempQueue.task_done()

def ipRange(inputAddress):
    octets = inputAddress.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))

def connectSocket(ip, port_number, delay, proto, outTcp, outUdp):
    eSocket = ''
    if proto.lower() == 't' or proto.lower == 'b':
        eSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        eSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        eSocket.settimeout(delay)

        try:
            eSocket.connect((ip, port_number))
            
            print "IP:", ip, "PORT:", port_number
            print eSocket.recvfrom(1024)
            outTcp[port_number] = 'Listening'
        except:
            outTcp[port_number] = ''
        
    if proto.lower() == 'u' or proto.lower() == 'b':
        eSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        eSocket.settimeout(4)
        try:
            eSocket.sendto("-HAXOR--", (ip, port_number))
            test, t2 = eSocket.recvfrom(1024)
        except socket.timeout:
            pass
            #print "%d/udp \tclosed" % (port_number)
        else:
            print "%d/udp \topen" % (port_number)
            outUdp[port_number] = 'Listening'
            pass
    eSocket.close()

def pingScan(host, sPort, ePort, delay):
    output = []
    for address in ipRange(host):
        t = threading.Thread(target=pingThreader, args=(sPort, ePort,  delay, output))
        t.daemon = True
        t.start()
        
    for address in ipRange(host):
        pingQueue.put(address)

    pingQueue.join()
    return output

def portScan(hosts, sPort, ePort, delay, proto):
    for address in hosts: 
        catString   = ''
        threadList  = []        
        outTcp      = {}
        outUdp      = {}
        sPortN      = int(sPort)
        ePortN      = int(ePort)
        rangeCount  = ePortN - sPortN
        count       = 0
        tempQueue   = Queue()
        
        for i in range(1024):
            t=threading.Thread(target=portThreader, args=(address, i, delay, tempQueue, proto, outTcp, outUdp))
            t.daemon=True
            t.start()
        
        for port in range(sPortN, ePortN):
            tempQueue.put(port)

        tempQueue.join()
        tempString = ''
        if proto.lower() == 't' or proto.lower() == 'b':
            for port in outTcp:
                if outTcp[port] == 'Listening':
                    tempString += "TCP Open: " + str(port) + "\n"
            
        if proto.lower() == 'u' or proto.lower() == 'b':
            for port in outUdp:
                if outUdp[port] == 'Listening':
                    tempString += "UDP Open: " + str(port) + "\n"

        if tempString:
            catString += "Scan: " + address + "[" + sPort + ":" + ePort + "]" + " Delay: " + str(delay) + "ms.\n"
            catString += tempString
            print catString
    
def main():
    desc = "Example usage: python PortScanner.py <ipAddress> 1 1000 10\nThe above example will scan the host \'<ipAddress>\' from port 1 to 1000 and wait 10ms\n"
    parser = argparse.ArgumentParser(description = desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('host',         metavar='H',                help='IP Address: 192.168.1.1-255')
    parser.add_argument('startport',    metavar='P1',   nargs='?',  help='Start scanning from this port')
    parser.add_argument('endport',      metavar='P2',   nargs='?',  help='Scan until this port')
    parser.add_argument('delay',        metavar='D',                help='Time delay on port couter')
    parser.add_argument('protocol',     metavar='P',                help='TCP or UDP or both t/u/b')
    
    args    = parser.parse_args()
    host    = args.host
    sPort   = args.startport
    ePort   = args.endport
    delay   = float(args.delay)
    proto   = args.protocol
    uoHosts = []
    #upHosts = pingScan(host, sPort, ePort, delay)
    upHosts = ipRange(host)
    portScan(upHosts, sPort, ePort, delay, proto)

if __name__ == '__main__':
    main()