import os,sys
import crypt
import codecs
from datetime import datetime,timedelta
import argparse
import hashlib
from multiprocessing import Process
import time
import Queue

today = datetime.today()


def reader(queue, user, crypted):
    print "Reader for: ", user
    while True:
        msg       = queue.get()
        ctype     = crypted.split("$")[1]
        if (msg == 'DONE'):
            break

        salt = crypted.split("$")[2]
        insalt = "$" + ctype + "$" + salt + "$"

        cryptWord = crypt.crypt(msg, insalt)
        
        if (cryptWord == crypted):
            time = str(datetime.today() - today)
            print "[+] Found password for the user: " + user + " ====> " + ctype + " ====> " + msg + " Time: "+time+"\n"
    
def writer(queue, dicList):
    for word in dicList:
        queue.put(word)
    queue.put('DONE')

def main():
   parse = argparse.ArgumentParser(description='Elliott\'s amazing /etc/shadow breaker.')
   parse.add_argument('-f', action='store', dest='path', help='Path to shadow file, example: \'/etc/shadow\'')
   argus=parse.parse_args()
   crypted  = ''
   user     = ''
   myDict   = {}
   dicList  = []
   dicFile   = open('password.lst','r')
    
   for word in dicFile.readlines():
       word = word.strip('\n')
       dicList.append(word)

   if argus.path == None:
       parse.print_help()
       exit
   else:
       passFile = open(argus.path,'r')
       for line in passFile.readlines():
            line = line.replace("\n","").split(":")
            if not line[1] in [ 'x', '*','!' ]:
                user    = line[0]
                crypted = line[1]
                myDict[user] = crypted

   for encrypts in myDict:
        queue = Queue.Queue()
        writer(queue, dicList)
        reader_p = Process(target=reader, args=(queue, encrypts, myDict[encrypts]))
        reader_p.daemon = True
        reader_p.start()
        
        _start = time.time()
#        reader_p.join()         # Wait for the reader to finish
    
   while True:
        pass
   
if __name__=="__main__":
   main()