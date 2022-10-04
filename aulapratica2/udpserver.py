import socket

localPort = 20001
bufferSize = 1024

msgFromServer = bytes("Hello UDP Client", 'utf-8')

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServerSocket.bind(('localhost', localPort))

print('O servidor UDP está pronto')

while (True):
      bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

      message = bytesAddressPair[0]
      address = bytesAddressPair[1]

      print("Mensagem: {}".format(message))
      print("Endereço IP do cliente: {}".format(address))
      
      UDPServerSocket.sendto(message, address)
