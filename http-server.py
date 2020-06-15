#! /usr/bin/env python3
# TCP Echo Server

import sys
import socket
import os
import time
import datetime

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
dataLen = 1000000
# Create a TCP "welcoming" socket. Notice the use of SOCK_STREAM for TCP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port:  ' + str(serverPort) + '\n')

# loop forever listening for incoming connection requests on "welcoming" socket
while True:
    # Accept incoming connection requests; allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    print("Socket created for client " + address[0] + ", " + str(address[1]))

    # Receive and print the client data in bytes from "data" socket
    data = connectionSocket.recv(dataLen).decode()
    #print(data)
    senddata=""
    strippeddata = data.split("\r\n")
    #print(strippeddata)
    filedata = strippeddata[0].split()
    filedata = filedata[1][1:]
    #print(filedata)
    getcurtime = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    if os.path.exists(filedata):
        
        if len(strippeddata) == 4:
            getftime= os.path.getmtime(filedata)
            utime = datetime.datetime.utcfromtimestamp(getftime).strftime("%a, %d %b %Y %H:%M:%S GMT\r\n")
            
            fle = open(filedata)
            fread = fle.read()
            flen = len(fread)
            senddata = "HTTP/1.1 200 OK\r\n\nDate: {}\r\nLast-Modified: {}\r\nContent-Length: {}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\\n\n{}\n".format(getcurtime,utime,flen,fread)
            
        else:
            compdata = strippeddata[2][19:]
            sentdate = datetime.datetime.strptime(compdata,"%a, %d %b %Y %H:%M:%S GMT")
            getftime= os.path.getmtime(filedata)
            utime = datetime.datetime.utcfromtimestamp(getftime).strftime("%a, %d %b %Y %H:%M:%S GMT")
            checkdate = datetime.datetime.strptime(utime,"%a, %d %b %Y %H:%M:%S GMT")
            deltadate = checkdate-sentdate 
            print(type(deltadate))
            if deltadate.total_seconds()<1:
                print("in")
                senddata="HTTP/1.1 304 Not Modified\r\nDate: {}\r\n \r\n".format(getcurtime)
                print(senddata)
                connectionSocket.send(senddata.encode())
            else:
                fle = open(filedata)
                fread = fle.read()
                flen = len(fread)
                senddata = "HTTP/1.1 200 OK\r\n\nDate: {}\r\nLast-Modified: {}\r\nContent-Length: {}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\\n\n{}\n".format(getcurtime,utime,flen,fread)


        #server checks the file to see if it exists,  conditional get req
    else:
        senddata="HTTP/1.1 404 Not Found\\r\\n\nDate: {}\r\nContent-Length: 0\r\n\r\n".format(getcurtime) 
 

    # Echo back to client
    print(senddata)
    connectionSocket.send(senddata.encode())

        
