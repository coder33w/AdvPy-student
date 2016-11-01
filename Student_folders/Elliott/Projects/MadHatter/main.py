from generators import tailFile
from generators import grepFile


def main():
    for log in tailFile('log'):
        for line in grepFile(log, '2222'):
            print line
        
        
if __name__ == "__main__":
    main()