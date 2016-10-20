def main():
    with open("sundb", "r") as f:
        myArray = []
        nf = open("images", "w")
        for line in f.readlines():
            items = line.split('/')
            if items[2]:
                if len(items) >= 5:
                    if '.' in items[3]:
                        myArray.append(items[2])
                    else:
                        string = items[2]+"/"+items[3]
                        myArray.append(string)
                else:
                    myArray.append(items[2])
        myDict = {};        counter = 0;
        for item in myArray:
            if myDict.has_key(item):
                myDict[item] += 1;
            else:
                myDict[item] = 1;
        for item in sorted(myDict):
            nf.write(item + " = " + str(myDict[item]) + "\n")
if __name__ == "__main__":
    main()