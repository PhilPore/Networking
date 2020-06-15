#! /usr/bin/env python3
# HTTP Client

import sys
import socket
import os

# Get the server hostname, port and data length as command line arguments
#host = sys.argv[1]
#port = int(sys.argv[2])
#count = int(sys.argv[3])

def GetReq1(packetdata,filenme):
    splitdata = packetdata.split("\r\n")
    #print(splitdata[2])
    #print(splitdata[-1])
    datemod = splitdata[2].split(": ")[1]
    cacheddata = "{}|{}".format(filename,datemod)
    #print(cacheddata)
    cachefile = open("cache1.txt","a+")
    cachefile.write(cacheddata) 

    
    #some sort of check to see if there is a 404 error. If so we terminate
    



url = sys.argv[1]
url_len = len(url)
splice_start = 0

host = url.split("/")[0].split(":")[0]
print(host)
port = int(url.split("/")[0].split(":")[1])
print(port)

filename = url.split("/")[1]
print(filename)
exi = os.path.exists("cache1.txt")


# Create TCP client socket. Note the use of SOCK_STREAM for TCP packet
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create TCP connection to server
print("Connecting to " + host + ", " + str(port))
clientSocket.connect((host, port))
GETpacket = "GET /{}  HTTP/1.1\r\nHost: {}:{}\r\n\r\n".format(filename, host,port)
if exi == False: #procs GET request 1
    clientSocket.send(GETpacket.encode())
    dataEcho = clientSocket.recv(1000000).decode()
    print(dataEcho)
    GetReq1(dataEcho,filename)
    if "404" in dataEcho.split("\r\n")[0]:
        print(dataEcho)
        exit()
    
else:
    cacher = open("cache1.txt")
    cread = cacher.read()
    if filename not in cread:
        clientSocket.send(GETpacket.encode())
        dataEcho = clientSocket.recv(1000000).decode()
        if "404" in dataEcho.split("\r\n")[0]:
            print(dataEcho)
            exit() 
        GetReq1(dataEcho,filename)
    else:
        
        timemod = ""
        cache = open("cache1.txt")
        lines = cache.readlines()
        for entry in lines:
            if filename in entry:
                timemod = entry.split("|")[1]
                break
        CGET = "GET /{}  HTTP/1.1\r\nHost: {}:{}\r\nIf-Modified-Since: {}\r\n\r\n".format(filename, host,port,timemod)
        clientSocket.send(CGET.encode())
        dataEcho = clientSocket.recv(1000000).decode()
        splitdata = dataEcho.split("\r\n")
        
        if "404" in splitdata[0]:
            print(dataEcho)
            exit()
        if "304" in splitdata[0]:
            print(dataEcho)
            exit() 

            #print(splitdata[2])
        else:   
            #print("IN HERE HAHAHA")
            datemod = splitdata[2].split(": ")[1]
            print(dataEcho)
            readdata = open("cache1.txt")
            cachelines = readdata.readlines()
            for i in range(len(cachelines)):
                if filename in cachelines[i]:  
                    cachelines[i].split("|")[1] = datemod
                    break
            editdata = open("cache1.txt","w")
            editdata.writelines(cachelines)

            
            


# Send encoded data through TCP connection

#clientSocket.send(data.encode())

clientSocket.close()
 




