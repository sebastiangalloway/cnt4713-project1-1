#!/usr/bin/env python3

import sys
import socket

def send(sock, msg):
    total_sent = 0
    while total_sent < len(msg):
        try:
            sent = sock.send(msg[total_sent:])
            if sent == 0:
                raise sock.error("ERROR: Connection broken")
            total_sent += sent
        except sock.error as e:
            sys.stderr.write("ERROR: sending data\n")
            sys.exit(1)

def receive(sock):
    msg = b""
    while b"\r\n" not in msg:
        chunk = sock.recv(10000)
        if not chunk:
            break
        msg += chunk
    return msg


        
        
def main():
    
    #sys.argv should look like --> python client.py <HOSTNAME-OR-IP> <PORT> <FILENAME>

    if len(sys.argv[1:]) != 3:
        sys.stderr.write("ERROR: Invalid number of arguments\n")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1:][1])
        if not(0 < port < 65535):
            sys.stderr.write("ERROR: Invalid port number\n")
            sys.exit(1)
    
    except ValueError:
        sys.stderr.write("ERROR: Non-integer port number\n")
        sys.exit(1)
    
    host = sys.argv[1:][0]
    filename = sys.argv[1:][2]
    
    connectTcp(host, port, filename)
    sys.exit(0)
  
if __name__ == '__main__':
    main()
