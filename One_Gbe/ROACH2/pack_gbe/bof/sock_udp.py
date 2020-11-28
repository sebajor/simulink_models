import socket
import sys

pkt_size = 36*220

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('10.0.0.29', 1234)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections

f = open('data', 'ab')

while True:
    # Wait for a connection
    try:

        # Receive the data in small chunks and retransmit it
        while True:
            data = sock.recv(pkt_size)
            f.write(data[:])
            #print('{!r}'.format(data))

    finally:
        # Clean up the connection
        f.close()
        sock.close()
