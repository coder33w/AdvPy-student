"""
###############################################################################
# FILE NAME : hackme.py
# AUTHOR : J.Enochs
# CREATION DATE : 21-Sep-2016
# LAST MODIFIED : 26-Sep-2016
# DESCRIPTION : Advanced python challenge.  This script takes a string and 
#               produces a hash code that gets appended to my name(Jason). The
#               challenge is to 1) decompile this script and then 2) alter it
#               so that is starts with the student's name instead of mine. Both
#               scripts must produce the same hash when presented with the same
#               input string.  This challenge is worth 15 flag points.
#               
###############################################################################/
"""
import pkgutil
import argparse
import hashlib
import os
from subprocess import Popen, PIPE

def main(store):
    count = 0
    bonus = False
    used_with = False

    if os.path.isfile('hackme.pyc'):
        os.chdir('/home/student/Projects/Advanced/')
        p = Popen(['./hackme.pyc', '-n', store], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        rc = p.returncode
    print "                                                   "
    print "                                                   "
    print "###################################################"
    print "                                                   "
    print "  Elliott-%s   " % output[63:103]
    print "                                                   "
    print "###################################################"
    print "                                                   "


    
        
    

if __name__ == '__main__':
    desc = "usage: %prog -n <random string>\n"
    p = argparse.ArgumentParser(description = desc, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("-n","--store", help="hackme help", action="store")
    args = p.parse_args()
    store = args.store
    main(store)
