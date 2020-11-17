# WebServer.py

from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np







from socket import *

serverPort = 8000   # server port
serverAddress = ""  # server address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(1000)   # 1000 = number of unexpected connection
print("Ready to server")

countad=0
countnum=0
fig = plt.figure()  # figure(도표) 생성

ax = plt.subplot(211, xlim=(0, 50), ylim=(0, 1024))

max_points = 50

line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float) * np.nan, lw=1, c='blue', ms=1)
countnum = countnum + countad


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
        for i in range(0, len(outputData), 8192):   # send buf size 1024
            connectionSocket.send(outputData[i:i + 8192])
        connectionSocket.send(b"\r\n\r\n")
        countad = countad + 1
        print(countad)

        connectionSocket.close()

    except IOError:
        # 404 Not Found
        header = "HTTP/1.1 404 Not found\r\n"
        headerBytes = bytes(header, "UTF-8")
        connectionSocket.send(headerBytes)
        countad=countad+1
        print(countad)


        def init():
            return line


        def animate(i):
            y = countnum
            old_y = line.get_ydata()
            new_y = np.r_[old_y[1:], y]
            line.set_ydata(new_y)
            print(new_y)
            return line


        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=50, blit=False)

        plt.show()

        connectionSocket.close()





