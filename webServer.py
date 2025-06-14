# import socket module
import socket
from socket import *
# In order to terminate the program
import sys

def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Accept only one connection at a time

    while True:
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024).decode()
            filename = message.split()[1]

            # Open and read the requested file
            with open(filename[1:], 'rb') as f:
                file_data = f.read()

            # Construct HTTP header
            header = b"HTTP/1.1 200 OK\r\n"
            header += b"Content-Type: text/html; charset=UTF-8\r\n"
            header += b"Server: MyPythonWebServer/1.0\r\n"
            header += b"Connection: close\r\n\r\n"

            # Send header + file content together
            connectionSocket.sendall(header + file_data)

        except Exception as e:
            # File not found or invalid request
            error_response = b"HTTP/1.1 404 Not Found\r\n"
            error_response += b"Content-Type: text/html; charset=UTF-8\r\n"
            error_response += b"Connection: close\r\n\r\n"
            error_response += b"<html><body><h2>404 Not Found</h2></body></html>"

            connectionSocket.sendall(error_response)

        connectionSocket.close()

if __name__ == "__main__":
    webServer(13331)
