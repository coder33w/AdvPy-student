import string
import base64
from Crypto import Random
from Crypto.Cipher import AES


def main():
    
    with open("ex4_1_data.txt", "r") as openFile:
        theLines = openFile.readlines()
        answer1  = rotConvert(theLines[0])
        answer2  = atbash(answer1[158:])
        answer3  = baseDecode(answer2[129:])
        answer4  = base128(answer3[196:])
        
def rotConvert(data):
    result  = ''
    base    = string.ascii_uppercase
    base1   = string.ascii_lowercase
    
    for letter in data:
        if letter.isalpha():
            if letter in base:
                basePosition        = base.index(letter)
                encodedPosition     = (basePosition - 6)
                result += base[encodedPosition]
            elif letter in base1:
                basePosition        = base1.index(letter)
                encodedPosition     = (basePosition - 6)
                result += base1[encodedPosition]

        else:
            result += letter
    print result
    return result

def atbash(data):
    result   = ''
    base     = string.ascii_uppercase
    key      = string.ascii_uppercase[::-1]
    base1    = string.ascii_lowercase
    key1     = string.ascii_lowercase[::-1]
    counter  = 0
    c2       = 0
    
    for letter in data:
        if letter in base:
            result += key[base.index(letter)]
        elif letter in base1:
            result += key1[base1.index(letter)]
        else:
            result += letter

    print result
    return result
    
def baseDecode(data):
    answer = base64.b64decode(data)
    print answer    
    return answer
    
    
def base128(data):
    print data
    aes = AES.new("9b4609b17fea63f3f3f067fc2f465c6e")
    answer = aes.decrypt(data)
    print answer
    return answer

##########################
if __name__ == "__main__":
    main()
##########################