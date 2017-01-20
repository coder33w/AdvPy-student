import mmap
import contextlib
import argparse

from Evtx.Evtx  import FileHeader
from Evtx.Views import evtx_file_xml_view
from lxml       import etree
from lxml.etree import XMLSyntaxError

def toLxml(recordXml):
    return etree.fromstring("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>%s" % 
                            recordXml.replace("xmlns=\"http://schemas.microsoft.com/win/2004/08/events/event\"", ""))
def ascii(s):
    return s.encode('ascii', 'replace').decode('ascii')

def printToAscii(buf):
    fh = FileHeader(buf, 0x0)
    print("<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"yes\" ?>")
    print("<Events>")
    for xml, record in evtx_file_xml_view(fh):
        print(ascii(xml))
    print("</Events>")

def getZero(xml):
    return toLxml(xml).xpath("/Event/EventData/Data[@Name]")[0].text
def getOne(xml):
    return toLxml(xml).xpath("/Event/EventData/Data[@Name]")[1].text
def getTwo(xml):
    return toLxml(xml).xpath("/Event/EventData/Data[@Name]")[2].text
def getThree(xml):
    return toLxml(xml).xpath("/Event/EventData/Data[@Name]")[3].text

def searchEvent(buf):
    taskList = {}
    fh = FileHeader(buf, 0x0)
    for xml, Record in evtx_file_xml_view(fh):
        try:
            record      = toLxml(xml).xpath("/Event/System/EventID")[0].text
            event       = toLxml(xml).xpath("/Event/System/Task")[0].text
            ctime       = toLxml(xml).xpath("/Event/System/TimeCreated")[0].get("SystemTime")
            taskAction  = toLxml(xml).xpath("/Event/EventData/Data")
            evZro       = ''
            evOne       = ''
            evTwo       = ''
            evThr       = ''
            
            try:
                evZro = getZero(xml)
            except:
                pass
            try:
                evOne = getOne(xml)
            except: 
                pass
            try:
                evTwo = getTwo(xml)
            except: 
                pass
            try:
                evThr = getThree(xml)
            except: 
                pass
            
            if record in taskList:
                taskList[record].append([record, ctime, event, taskAction, evZro, evOne, evTwo, evThr])
            else:
                taskList[record] = [[record, ctime, event, taskAction, evZro, evOne, evTwo, evThr]]
        
        except(etree.XMLSyntaxError, IndexError) as e:
            continue
    return taskList

def main(args):
    taskList = {}
    with open(args.evtx, 'r') as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
            fh = FileHeader(buf, 0x0)
            if args.toXml.lower() == "y":
                printToAscii(buf)

            taskList = searchEvent(buf)

    for event in taskList:
        print "\nEVENT:", event
        if event == '4776': # Invalid Logon Attempt
            print "-----: [ Bad Logon Attempt ]"
            print "----------------------------"

        if event == '4624': # Successfully Logged on
            print "-----: [ Successful Logon  ]"
            print "----------------------------"

        if event == '1102': # Successful Audit
            print "-----: [ Successful Audit  ]"
            print "----------------------------"

        if event == '4672': # Special Privledges
            print "-----: [ Special Privleges ]"
            print "----------------------------"

        if event == '4634': # Account Logged Off
            print "-----: [ Successful Logoff ]"
            print "----------------------------"

        for subVent in taskList[event]:
            print '[{}] {:>20} {:>30} {:>20}'.format(subVent[1], subVent[5], subVent[6], subVent[7])
    
    count = []
    for events in taskList:
        for event in taskList[events]:
            if events == '4776': 
                count.append(event[5])
    print set(count)
    print len(set(count))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Parse through a .EVTX file")
    parser.add_argument("evtx", type=str, help="Path to the Windows EVTX event log file")
    parser.add_argument("toXml", type=str, help="[Y/N] print XML of EVTX log")
    args = parser.parse_args()
    main(args)