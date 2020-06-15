#Philip Poretsky | ptp24 | Section 356-002

import sys
import struct
from struct import *
import socket
import random

ServIP = sys.argv[1]
ServHost = int(sys.argv[2])
Hostname = sys.argv[3]
Htype = sys.argv[4]
Hin = sys.argv[5]

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)

Sucher_Hir = Hostname + " " + Htype + " " + Hin
ranval = random.randint(1, 100)
packr = struct.Struct("! hhihh{}s".format(len(Sucher_Hir)))
encDat = Sucher_Hir.encode()
Sund = packr.pack(1, 0, ranval, len(encDat), 0, encDat)


print("Sending Request to {}, {}:\n".format(ServIP, ServHost))
print("Message ID:   {}\n".format(ranval))
print("Question Length: {} bytes\n".format(len(encDat)))
print("Answer Length: {} bytes\n".format(len("")))
print("Question: {}\n".format(Sucher_Hir))
for i in range(3):
    try:
        clientsocket.sendto(Sund, (ServIP, ServHost))

        dataEcho, address = clientsocket.recvfrom(1024)

        initunpack = unpack_from("! hhihh", dataEcho)
       # print(initunpack) wanted to see the tuple
        strrec = unpack_from("{}s{}s".format(initunpack[3], initunpack[4]), dataEcho[12:]) 
        query = strrec[0].decode()
        answr = strrec[1].decode()
        #data is basically a string so everytihng else is a total 12 bytes
        #In a real life setting , we'd wanna double check to see if everything is right
        #print(strrec)
        if initunpack[1] == 1:
            print("Recieved Message from {}, {}:\n".format(ServIP, ServHost))
            print("Return Code: {} (Name does not exist)\n".format(initunpack[1]))
            print("Message ID:   {}\n".format(initunpack[2]))
            print("Question Length: {} bytes\n".format(len(query)))
            print("Answer Length: {} bytes\n".format(len(answr)))
            print("Question: {}\n".format(query))
        else:
            print("Recieved Message from {}, {}:\n".format(ServIP, ServHost))
            print("Return Code: {} (No errors)\n".format(initunpack[1]))
            print("Message ID:   {}\n".format(initunpack[2]))
            print("Question Length: {} bytes\n".format(len(query)))
            print("Answer Length: {} bytes\n".format(len(answr)))
            print("Question: {}\n".format(query))
            print("Answer: {}\n".format(answr))
        break
    except socket.timeout:
        errmsg =""
        if i != 2:
            errmsg = "\nSending Request to {}, {}:\n".format(ServIP, ServHost)
        else:
            errmsg= " Exiting program.\n"
        print("Request timed out...{}".format(errmsg))


    


    

clientsocket.close()
