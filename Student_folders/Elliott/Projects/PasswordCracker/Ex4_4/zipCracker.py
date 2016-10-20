import zipfile
import string

def generateWords():
    charlist = string.ascii_lowercase
    charlist += "!@#"
    charlist += string.digits
    
    answer = '....'
    
    for letter in charlist:
        t = list(answer)
        t[0] = letter
        answer = ''.join(t)
        for letter in charlist:
            t = list(answer)
            t[1] = letter
            answer = ''.join(t)
            for letter in charlist:
                t = list(answer)
                t[2] = letter
                answer = ''.join(t)
                for letter in charlist:
                    t = list(answer)
                    t[3] = letter
                    answer = ''.join(t)
                    yield answer

def main():

    zip = zipfile.ZipFile("ex4_4.zip")
    for word in generateWords():
        try:
            zip.extractall(pwd=word)
            print "Woot", word
            break
        except:
            pass
        

if __name__ == '__main__':
    main()