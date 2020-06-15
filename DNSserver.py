#Philip Poretsky | ptp24 | Section 356-002

import sys
import socket
import struct
from struct import *
import random
import time


serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket


serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
# save the names from the doc into some data structure. A dictionary can be acceptable. Lookup table.
fr = open("dns-master.txt")
dnsdict = {}

for line in fr:
    if line[0] == "#" or line == "\n":
        continue
    templ = line.split()
    dictkey = templ[0] + " " + templ[1] + " " + templ[2]
    dnsdict[dictkey] = line[:-1]
    # tempstruct = struct.Struct()
#print(dnsdict)

packrec = struct.Struct("!hhihh")
while True:
    data, address = serverSocket.recvfrom(1024)
    decdat = packrec.unpack_from(data)
    #print(decdat)   
    strgetr = unpack_from('{}s'.format(decdat[3]),data[12:])
    #print(strgetr)
    searcher = strgetr[0].decode()
    unpackdat = packrec.unpack_from(data)
    #print(unpackdat)
    
    if searcher not in dnsdict.keys():
        #print("Element not in table\n")
        repackr = struct.Struct("!hhihh{}s".format(len(searcher)))
        encod = searcher.encode()
        Sund = repackr.pack(2, 1, unpackdat[2], len(encod), 0, encod)
        #serverSocket.sendto(Sund, (address))
    else:
        repackr = struct.Struct(
            "! hhihh{}s{}s".format(len(searcher), len(dnsdict[searcher]))
        )
        #print(dnsdict[searcher])
        encodr = searcher.encode()
        dnscod = dnsdict[searcher].encode()
        Sund = repackr.pack(
            2, 0, unpackdat[2], len(encodr), len(dnsdict[searcher]), encodr, dnscod,
        )
        #serverSocket.sendto(Sund, (address))


# lenget = tempstruct.unpack_from('!!hhihh', data)
# strget = tempstruct.unpack('!{}s'.format(lenget[4]),data[12:] )
