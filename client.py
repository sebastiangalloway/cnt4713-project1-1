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

def connectTcp(host, port, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        try:
            sock.connect((host, port))
            msg = receive(sock)
                        
            if msg == b"accio\r\n":
                send(sock, b"confirm-accio\r\n")                
                msg = receive(sock)
                
                if msg == b"accio\r\n":
                    send(sock, b"confirm-accio-again\r\n")
                    send(sock, b"\r\n")
                    
                    try:
                        with open(filename, "rb") as f:
                            while True:
                                content = f.read(10000)
                                if not content:
                                    break
                                send(sock, content)
                                break
                        f.close()
                    except FileNotFoundError:
                        sys.stderr.write("Error: File not found\n")
                        sys.exit(1)
                else:
                    sys.stderr.write("Error: Invalid data from the server\n")
                    sys.exit(1) 
            else:
                sys.stderr.write("Error: Invalid data from the server\n")
                sys.exit(1)
            #print("Connection Succeeded")
        except Exception as e:
            sys.stderr.write("ERROR: Connection failed")
            sys.exit(1)           
        finally:   
            sock.close()
        
        
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
