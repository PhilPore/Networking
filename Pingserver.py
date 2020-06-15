#Philip Poretsky | ptp24 | Section 356-002
import sys
import socket
import random
import struct
import time

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket


serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    ranval = random.randint(1,10)
    # Receive and print the client data from "data" socket
    AcqDat = struct.Struct('! i I') #network byte order is big endian. But little endian is better for processing
    data, address = serverSocket.recvfrom(AcqDat.size)
    NewData = AcqDat.unpack(data) #We get a tupple
    print("Responding to ping request with sequence number {}".format(NewData[1]))
    if ranval < 4:
        print("Message with sequence number: {} dropped\n".format(NewData[1]))
        continue
    Recdata = AcqDat.pack(2, NewData[1])
    #recieve from client and unpack data ^ Needs to be fixed
    # respond to client with packed data and seq number 2
    serverSocket.sendto(Recdata,(address)) #address is a tuple, so you can just send it. Cool stuff
