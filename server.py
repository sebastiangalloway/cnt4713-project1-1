#!/usr/bin/env python3

import socket, sys

class Server:
    def __init__(self, sock = None, secs = 10):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        
        self.sock.settimeout(secs)
    
    def connect(self, port, host = "0.0.0.0"):
        try:
            self.sock.bind((host, port))
            self.sock.listen(10)
        except socket.error as msg:
            self.sock.close()
            sys.stderr.write("ERROR: %s\n" % msg)
            sys.exit(1)

        connection, address = self.sock.accept()
        data = ""
                
        with connection:
            try:
                data += connection.recv(4096)
                print(data)
                connection.send(b"Successfully connected to server")
            except socket.error as msg:
                self.sock.close()
                connection.close()
                sys.stderr.write("ERROR: %s\n" % msg)
                sys.exit(1)
            finally:
                self.sock.close()
                connection.close()
                
def main():
    # Command line arguments format:
    # python3 server.py <PORT> <FILE-DIR>
    
    if len(sys.argv) != 3:
        sys.stderr.write("ERROR: Invalid number of arguments\n")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("ERROR: Non-integer port number\n")
        sys.exit(1)
        
    if port < 1 or port > 65535:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)
        
    file_directory = sys.argv[2]
    
    s = Server()
    s.connect(port)
    
if __name__ == '__main__':
    main()
