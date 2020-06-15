#Philip Poretsky | ptp24 | Section 356-002

import sys
import socket
import random
import struct
import time
# Get the server hostname, port
host = sys.argv[1]
port = int(sys.argv[2])

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
print("Pinging {}, {}:".format(host,port))
counter = 0
min = sys.maxsize
max = -min-1
for i in range(10):
    data = struct.Struct('! I I')
    Sendr = data.pack(1, i+1)
    try:
        #we read the time
        print("Ping message number {} ".format(i+1))
        start = time.perf_counter()
        clientsocket.sendto(Sendr,(host, port))
        dataEcho, address = clientsocket.recvfrom(data.size)
        #We use data's size to know what to recieve 1024 was just byte size
        finish = time.perf_counter()
        RTT = finish - start
        print("RTT: {}\n".format(RTT))
        if RTT > max:
            max = RTT
        if RTT < min:
            min = RTT
    except socket.timeout:
            print( " timed out\n")
            counter+=1
            continue

print("Sent: 10 | Recieved: {} | Percent Loss {}%\n".format(10-counter, (counter/10)*100))
print("Max TTL: {} | Min TTL:{}".format(max, min))


clientsocket.close()
