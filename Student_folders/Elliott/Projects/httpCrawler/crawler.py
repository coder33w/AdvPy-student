from bs4 import BeautifulSoup
import sys
import requests

myList = {}

def get_links(url, haveCookie, cookie):
    print url, "->",myList[url]
    yarp = haveCookie
    cooks = cookie
    if myList[url] == 0:
        myList[url] = 1

        if haveCookie:
            r = requests.get(url, cookies=cookie)
        else:
            r = requests.get(url)
            cooks = r.cookies
            yarp = True

        contents = r.content
        soup = BeautifulSoup(contents, "lxml")
        links = soup.findAll('a')
        if "key" in contents and len(links) == 0:
            print "FOUND KEY:", contents
        for link in links:
            try:
                test = str(link).split('\"')[1]
                myList[test] = 0
                get_links(test, yarp, cooks)
            except Exception as e:
                pass
    else:
        print "Already seen ->", url

if __name__ == "__main__":
    myList["http://10.0.0.210:8084"] = 0
    haveCookie = False
    cookie = ''
    get_links("http://10.0.0.210:8084", haveCookie, cookie)
    sys.exit()