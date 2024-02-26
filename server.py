import socket
import sys
import signal
import time

# define signal handler function
def signal_handler(signal, frame):
    global not_stopped
    print('Exiting gracefully...')
    not_stopped = False
    sys.exit(0) # exit with code 0

# register signal handlers
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# parse command line arguments
if len(sys.argv) < 2:
    sys.stderr.write("ERROR: Missing port number\n")
    sys.exit(1)

try:
    port = int(sys.argv[1])

except ValueError:
    sys.stderr.write("ERROR: Invalid port number\n")
    sys.exit(1)

if port > 65535:
    sys.stderr.write("ERROR: Invalid port number\n")
    sys.exit(1)

if port < 0:
    sys.stderr.write("ERROR: Invalid port number\n")
    sys.exit(1)



def server_program():
    # get the hostname
    host = socket.gethostname()
    port = int(sys.argv[1])  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(10)
    client_socket, server_address = server_socket.accept()  # accept new connection

    client_socket.settimeout(10)

        # send accio command to the client
    #conn.send(b'accio\r\n')


    #print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = client_socket.recv(1024)#.decode()
        if not data:
            # if data is not received break
            break
        #print("from connected user: " + str(data))
        #data = input(' -> ')

    client_socket.send(b'accio\r\n')
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = client_socket.recv(1024)#.decode()
        if not data:
            # if data is not received break
            break
        #print("from connected user: " + str(data))
        #data = input(' -> ')

    client_socket.send(b'accio\r\n')
        #conn.send(data.encode())  # send data to the client

    client_socket.close()  # close the connection


if __name__ == '__main__':
    server_program()
