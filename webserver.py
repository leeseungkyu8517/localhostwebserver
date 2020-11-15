# WebServer.py

from socket import *

serverPort = 8000   # server port
serverAddress = ""  # server address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(1000)   # 1000 = number of unexpected connection
print("Ready to server")


while True:
    connectionSocket, address = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)   # buf size 1024
        print("Message : " + str(message))
        # exception when message is null
        if not message:
            continue
        filename = message.split()[1]
        f = open(filename[1:], "rb")
        outputData = f.read()
        # 200 OK
        header = "HTTP/1.1 200 OK\r\n\r\n"
        headerBytes = bytes(header, "UTF-8")
        connectionSocket.send(headerBytes)
        # when buf size is 1 can't parse html code
        for i in range(0, len(outputData), 1024):   # send buf size 1024
            connectionSocket.send(outputData[i:i + 1024])
        connectionSocket.send(b"\r\n\r\n")
        connectionSocket.close()
    except IOError:
        # 404 Not Found
        header = "HTTP/1.1 404 Not found\r\n"
        headerBytes = bytes(header, "UTF-8")
        connectionSocket.send(headerBytes)
        connectionSocket.close()