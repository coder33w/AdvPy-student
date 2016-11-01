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

def ipRange(inputAddress):
    octets = inputAddress.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))

def connectSocket(ip, cPort, lPort, delay, proto, outTcp, outUdp):
    eSocket = ''
    if proto.lower() == 't' or proto.lower == 'b':
        eSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        eSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        eSocket.settimeout(delay)
        try:

            eSocket.bind(('0.0.0.0', lPort))
            eSocket.connect((ip, cPort))        
            print "IP:", ip, "PORT:", cPort
            answered = eSocket.recvfrom(1024)
            print "Answered:", answered
            
            answered = answered[0].split('\n')
            answered = answered[0].split(',')
            print "Test", answered
            
            print "Trying to connect to:", answered[0]
            try:
                connectSocket(ip, int(answered[0]), int(answered[1]), delay, proto, outTcp, outUdp)
            except Exception as e:
                print "Error on 2nd connect: ", e
            
            outTcp[cPort] = ''
        except Exception as e:
            print "Error loc 1:", e
        
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

def portScan(hosts, cPort, lPort, delay, proto):
    for address in hosts: 
        catString   = ''
        threadList  = []        
        outTcp      = {}
        outUdp      = {}
        lPortN      = int(lPort)
        cPortN      = int(cPort)
        count       = 0
        tempQueue   = Queue()

        try:    
            connectSocket(hosts, cPortN, lPortN, delay, proto, outTcp, outUdp)
        except Exception as e:
            print "Error:", e
            pass
        
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
            catString += "Scan: " + address + "[" + lPort + "->" + cPort + "]" + " Delay: " + str(delay) + "ms.\n"
            catString += tempString
            print catString
    
def main():
    desc = "Example usage: python PortScanner.py <ipAddress> 1 1000 10\nThe above example will scan the host \'<ipAddress>\' from port 1 to 1000 and wait 10ms\n"
    parser = argparse.ArgumentParser(description = desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('host',         metavar='H',                help='IP Address: 192.168.1.1-255')
    parser.add_argument('port',         metavar='P1',   nargs='?',  help='Start scanning from this port')
    parser.add_argument('locPort',      metavar='P2',   nargs='?',  help='Scan until this port')
    parser.add_argument('delay',        metavar='D',                help='Time delay on port couter')
    parser.add_argument('protocol',     metavar='P',                help='TCP or UDP or both t/u/b')
    
    args    = parser.parse_args()
    host    = args.host
    cPort   = args.port
    lPort   = args.locPort
    delay   = float(args.delay)
    proto   = args.protocol

    portScan(host, cPort, lPort, delay, proto)

if __name__ == '__main__':
    main()