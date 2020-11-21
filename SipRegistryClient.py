import time
import socket

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the remote host and port
sock.connect(('127.0.0.1', 8888))

# Send a request to the host
sock.send("01574393bae33557c3000100620007".encode('utf-8'))

# Get the host's response, no more than, say, 1,024 bytes
response_data = sock.recv(1024)

print(response_data)

# Terminate
sock.close(  )
