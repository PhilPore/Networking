#! /usr/bin/env python3
# Echo Client
import sys
import socket

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
count = int(sys.argv[3])
data = 'X' * count # Initialize data to be sent

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(1)
# Send data to server


# Receive the server response. Try catch here. the .timeout feature might be useful
    #dataEcho, address = clientsocket.recvfrom(count)
  #  print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())

for i in range(3):
    try:
        print("Sending data to   " + host + ", " + str(port) + ": " + data +" (" +str(count) + " characters)")
        clientsocket.sendto(data.encode(),(host, port))
        dataEcho, address = clientsocket.recvfrom(count)
        print("Receive data from " + address[0] + ", " + str(address[1]) + ": " + dataEcho.decode())
        break
 
    except socket.timeout:
        print("Message timed out\n")
          

#Close the client socket
clientsocket.close()
  
