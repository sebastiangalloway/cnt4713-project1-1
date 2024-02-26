#!/usr/bin/env python3

import time
import sys
import socket

def validatePort(port):
    if not isinstance(port, int):
        sys.stderr.write("ERROR: Port is not an integer!")
        sys.exit(1)

    if not 1 <= port <= 65535:
        sys.stderr.write("ERROR: Port is not valid range.")
        sys.exit(1)



class client:
    domain_name = 0
    host_port = 0
    file_name = 0

    def __init__(self):
        self.domain_name = sys.argv[1]
        self.host_port = int(sys.argv[2])
        self.file_name = sys.argv[3]

    def makeConnection(self):
        connection = 0
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error as err:
            sys.stderr.write("ERROR: Socket Creation failed!")
            sys.exit(1)
            return False

        try:
            self.domain_name = socket.gethostbyname(self.domain_name)

        except socket.gaierror:
            sys.stderr.write("ERROR: The host could not be reached!")
            sys.exit(1)


        try:
            validatePort(self.host_port)

        except socket.error as err:
            sys.stderr.write("ERROR: Port is not in valid rang4e!")
            sys.exit(1)

        try:

            sys.stderr.write("ERROR: ")
            connection.settimeout(10)
            connection.connect((self.domain_name, self.host_port))
            while True:
                data = connection.recv(1024)
                if data:
                    stuff = connection.send(b'confirm-accio\r\n')

                    while True:
                        data1=connection.recv(1024)
                        if data1:
                            stuff2 = connection.send(b'confirm-accio-again\r\n')
                            break
                    break

            stuff2 = connection.send(b'\r\n')

            sendfile = open(self.file_name, "rb")

            while True:
                sendbytes = sendfile.read(10000)
                if len(sendbytes) == 0:
                    break
                connection.send(sendbytes)



        except socket.error:
            print("ERROR: Connection failed!")
            sys.exit(1)
            return False






host = client()
host.makeConnection()
