"""Web server capable of responding to a single request."""
from socket import *  # Import socket module
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket.
serverPort = 80
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(4096).decode()
        filename = message.split()[1]
        if filename == '/':
            filename = '/index.html'
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        # Send one HTTP header line into socket
        header = 'HTTP/1.0 200 OK\r\n\r\n'
        connectionSocket.send(header.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.close()
    except OSError:
        # Send response message for file not found
        response = 'HTTP/1.0 404 NOT FOUND\n\n<html><head></head><body><h1>404 Not Found</h1></body></html>'
        connectionSocket.sendall(response.encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
