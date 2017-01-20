import re, os

def tailFile(fileName):
    firstCall = True
    print "Opening", fileName
    while True:
        try:
            with open(fileName) as input:
                if firstCall:
                    input.seek(0,2)
                    firstCall = False
                latestData = input.read()
                
                while True:
                    if '\n' not in latestData:
                        latestData += input.read()
                        if '\n' not in latestData:
                            yield ''
                            if not os.path.isfile(fileName):
                                break
                            continue
                        latestLines = latestData.split('\n')
                        if latestData[-1] != '\n':
                            latestData = latestLines[-1]
                        else:
                            latestData = input.read()
                        for line in latestLines[:-1]:
                            yield line + '\n'
        except IOError:
            yield '' 
            
def grepFile(line, pattern):
    matches = 0
    if pattern in line:
        matches += 1
        yield line.strip()