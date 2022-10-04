import socket

localPort = 20001
bufferSize = 1024

msgFromServer = bytes("Hello UDP Client", 'utf-8')

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind(('localhost', localPort))

UDPServerSocket.sendto(msgFromServer,UDPServerSocket.recvfrom(bufferSize)[1])

print('O servidor UDP está pronto')

while (True):
      bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
      address = bytesAddressPair[1]
      message = bytesAddressPair[0]
      UDPServerSocket.sendto(message, address)