#!/usr/bin/env python
# -*- coding: utf-8 -*-
from astropy.io import ascii
from sys import getsizeof
import struct


def main():
    data = ''

    with open("table1.dat", "r") as file:
        data = ascii.read(file)
        print "\n\n(2)  Print the entire ascii table (Ex1_4_h3)"
        print "==================================\n"
        print data
        
        print "\n\n(3)  Print only the column RAdeg (Ex1_4_h4)"
        print "==================================\n"
        print data['RAdeg']
        
        print "\n\n(4)  Print only row 4 (Ex1_4_h5)"
        print "=================================="
        print data['RAdeg'][4]
    
        print "\n\n(Bonus)(Ex1_4_h6)"
        print "=================================="
    
        f = open("day1.txt", "w")
        
        f.write("         Type: " + str(data['ID'].dtype) + "\n")
        f.write("         Size: " + str(getsizeof(data['ID'].dtype))+ "\n")
        f.write("Little Endian: " + str(struct.unpack('<I', struct.pack('=I', 1))[0] == 1)+ "\n")
        f.close()
        
        f = open("day1.txt", "r")
    
    with open("values.dat", "w") as file:
        ascii.write(data, file)
    
        for line in f:
            print line
        
if __name__ == "__main__":
    main()