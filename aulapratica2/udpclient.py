import socket

msgFromClient = bytes("Hello UDP Server", 'utf-8')
serverAddressPort = ('localhost', 20001)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.sendto(msgFromClient, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

print('Message from Server {}'.format(msgFromServer[0]))