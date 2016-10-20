
import sys
import traceback

from netaddr import IPNetwork
from netaddr import IPSet
from threading import  Thread                                                                                       
import thread

from IPScanner import asyncScanner
from Scavenger import SMBScavenger
from twisted.internet import reactor

#1 fast scavenge 
#2 deep scavenge

# Once we find an smb server, we scavenge it.

def test_result(host):
    SMBScavenger(host)
    
class Scavenge(Thread):
    def __init__(self, host):
        Thread.__init__(self)
        self.host = host
        
    def run(self):
        print "Starting " + self.host
        test_result(self.host)
        print "Exiting " + self.host

if __name__ == "__main__":
    try:
        #1 get ip range from argument, 
        ipn = IPNetwork(sys.argv[1])
        ports = [int(sys.argv[2])]
        subnets = IPSet(ipn)
        ips = []
        for ip in subnets:
            ips.append(str(ip))
        
        #2 Scan all the addresses in that range at given port. 
        # TODO: create a max amount of sockets allowed at the same time
        scan = asyncScanner(ips, ports, 4)
        reactor.run()
        results = scan.get_results()
        # TODO: make it stop when scanning...
        td = [] 
        if len(results) > 0:
            print 'Found ' + str(len(results)) + ' results.'
            ## create a scavenger thread for each result. 
            for result in results:
                print 'Now Thread Scavenging:', result[0], result[1]
                t = Scavenge(result[0])
                td.append(t)
                
            # Start all threads 
            for x in td:
                x.start()
                x.join()
                #print 'Now Scavenging:', result[0], result[1]
                ##getShare(result[0])
                #SMBScavenger(result[0])
 
    except:
        print traceback.format_exc()
        
        
        
        
        
        
        


        
        
        
        
