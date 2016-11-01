import pcapy
from impacket import ImpactDecoder

def Process(header, data):
    decoder = ImpactDecoder.EthDecoder()
    ether = decoder.decode(data)
    
    ipHeader = ether.child()
    packetType = ipHeader.child().protocol
    tcpHeader = ''
    if packetType == 6:
        tcpHeader = ipHeader.child()

    print "{:15}[{:5}] ----> {:15}[{:5}] [-{}-{}-{}-{}-{}-]".format(ipHeader.get_ip_src(), 
                                                       tcpHeader.get_th_sport(), 
                                                       ipHeader.get_ip_dst(), 
                                                       tcpHeader.get_th_dport(), 
                                                       ("S" if tcpHeader.get_SYN() else " "),
                                                       ("A" if tcpHeader.get_ACK() else " "),
                                                       ("U" if tcpHeader.get_URG() else " "),
                                                       ("P" if tcpHeader.get_PSH() else " "),
                                                       ("R" if tcpHeader.get_RST() else " ")
                                                       )
    payload = getPayload(tcpHeader)
    return

def getPayload(tcpHeader):
    payloadDec = tcpHeader.child().get_bytes().tolist()
    ascii = []
    
    for decByte in payloadDec:
        if decByte in range(9,14) or decByte in range(32,127):
            hexByte = str(hex(decByte)).lstrip("0x")
            
            if len(hexByte) == 1:
                hexByte = "0" + hexByte
            asciiByte = hexByte.decode('hex')
            ascii.append(asciiByte)
            
    payloadAscii = ''.join(ascii)
    return payloadAscii
            

def main():
    reader = pcapy.open_offline("ex7_2_traffic.pcap")
    reader.loop(0,Process)

if __name__ == '__main__':
    main()