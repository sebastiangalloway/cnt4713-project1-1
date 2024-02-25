import socket, sys
        
def send(socket, msg):
    total_sent = 0
    while total_sent < len(msg):
        sent = socket.send(msg[total_sent:])
        if sent == 0:
            raise RuntimeError("ERROR: Socket connection broken\n")
        total_sent += sent
    #print("Sent:", msg)
    #print("Total sent:", total_sent)

def receive(socket, str):
    msg = b""
    while str not in msg:
        chunk = socket.recv(4096)
        if not chunk:
            break
        msg += chunk
    #print("Received:", msg)
    return msg

def connect(port, host = "0.0.0.0"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        
    except socket.error as msg:
        sock.close()
        sys.stderr.write("ERROR: Connection failed")
        sys.exit(1)
        
    while True:        
        try:
            sock.settimeout(10)
            sock.listen(10)
            connection, address = sock.accept()
            connection.settimeout(10)
                        
        except socket.error as msg:
            sock.close()
            sys.stderr.write("ERROR: %s\n" % msg)
            sys.exit(1)
        
        send(connection, b"accio\r\n")
        msg = receive(connection, b"confirm-accio\r\n")
        
        if msg == b"confirm-accio\r\n":
            send(connection, b"accio\r\n")
            msg = receive(connection, b"\r\n")
            
            if msg == b"confirm-accio-again\r\n":
                msg = receive(connection, b"\r\n")                                                                                            
                sock.close()
                connection.close()
                sys.exit(0)
            else:
                sock.close()
                connection.close()
                sys.stderr.write("ERROR: Invalid data\n")
                sys.exit(1)

        else:
            sock.close()
            connection.close()
            sys.stderr.write("ERROR: Invalid data\n")
            sys.exit(1)

def main():
    # Command line arguments format:
    # python3 server-s.py <PORT>
    
    if len(sys.argv) != 2:
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

    connect(port)
    
if __name__ == '__main__':
    main()
