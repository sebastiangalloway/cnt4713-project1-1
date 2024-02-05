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


  
if __name__ == '__main__':
    main()
