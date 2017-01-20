import re
import string
from operator import pos


def regParse(allLines):
    socials     = []
    phones      = []
    ips         = []
    crap        = []
    
    socialRe    = r"^(\d{3})[\s-]?(\d{2})[\s-]?(\d{4})$"
    phoneRe     = r"\(?([0-9]{3})\)?([ \/.-]?)([0-9]{3})\2([0-9]{4})$"
    ipRe        = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    
    for line in allLines:
        setSkip = False
        for letter in string.ascii_letters:
            if letter in line:
                crap.append(line)
                setSkip = True
                break

        if not setSkip:
            if re.match(ipRe, line):
                ips.append(line)
            elif re.match(phoneRe, line):
                phones.append(line)
            elif re.match(socialRe, line):
                socials.append(line)
            else:
                crap.append(line)
            
    return socials, phones, ips, crap

def parsePhones(phones):
    nums = ['0','1','2','3','4','5','6','7','8','9']
    cleanedList = []
    result = ''
    for phone in phones:
        count = 0
        pos   = 0
        ecount= 0
        for number in phone:
            if number in nums:
                ecount += 1
        if ecount == 10:
            result += '('
        else:
            result += '      '
                
        for number in phone:
            if number in nums:

                count = count + 1
                result += number
                if count is 3 and pos is 0:
                    if ecount == 10:
                        result += ') '
                    else:
                        result += '-'
                    count = 0
                    pos = 1
                    
                if count == 3 and pos == 1 and ecount == 10:
                    result += '-'
                    count = 0
                    pos = 2
        if len(result.split('-')[1]) == 4:
            cleanedList.append(result)
        result = ''
    return cleanedList

def parseSocials(socialSecurity):
    cleanedList = []
    nums = ['0','1','2','3','4','5','6','7','8','9']
    result = ''
    for line in socialSecurity:
        count = 0
        pos   = 0
        for letter in line:
            if letter in nums:
                count = count + 1
                result += letter
                if count is 3 and pos is 0:
                    result += '-'
                    count = 0
                    pos =    1
                    
                if count == 2 and pos == 1:
                    result += '-'
                    count = 0
                    pos = 2
        cleanedList.append(result)
        result = ''


    for social in cleanedList:
        if social == '078-05-1120':
            print "Error:", social, "is invalid. Removing"
            cleanedList.remove(social)
        
        socSplit = social.split('-')
        for oct in socSplit:
            if len(oct) == 3:
                if int(oct) in xrange(900,1000) or oct == '000' or oct == '666':
                    print "Error:", social, "is invalid."
                    cleanedList.remove(social)            
            if len(oct) == 4:
                if oct == '0000':
                    print "Error:", social, "is invalid."
                    cleanedList.remove(social)
            if len(oct) == 2:
                if oct == '00':
                    print "Error:", social, "is invalid."
                    cleanedList.remove(social)
            if len(oct) > 4:
                print "Error:", social, "is invalid."
                cleanedList.remove(social)
    return cleanedList

def parseIps(ipAddress):
    cleanedList = []
    for ip in ipAddress:
        use = True
        octets = ip.split('.')
        for oct in octets:
            if int(oct) >= 256:
                use = False
        
        if use == True:
            cleanedList.append(ip)
    return cleanedList

def main():
    allLines = []
    with open ("ex4_2_data.txt", "r") as regFile:
        allLines = regFile.readlines()
    
    socialSecurity, phoneNumber, ipAddress, crap = regParse(allLines)
    
    socialSecurity  = parseSocials(socialSecurity)    
    
    print "\nSoc:", len(socialSecurity), "     Expected: 1422"

    phoneNumber     = parsePhones(phoneNumber)  
    print "Phn:", len(phoneNumber), "     Expected: 1403"
    ipAddress       = parseIps(ipAddress)
    print "Ips:", len(ipAddress), "     Expected: 1398"

if __name__ == "__main__":
    main()