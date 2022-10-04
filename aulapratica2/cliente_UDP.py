from itertools import count
import socket
import time

msgFromClient = bytes("Hello UDP Server", 'utf-8')
serverAddressPort = ('localhost', 20001)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.sendto(msgFromClient, serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)

print("Handshaking: {}".format(msgFromServer))
tempo = 15

def check(msgfromServer):
      return msgFromServer == str(b'#10')
            
for i in range(1,11,1):
      msgFromClient = bytes("#{}".format(str(i)), 'utf-8')
      UDPClientSocket.sendto(msgFromClient,serverAddressPort)
      msgFromServer = UDPClientSocket.recvfrom(bufferSize)
      if i == 10:
            if msgFromServer[0] == bytes('#{}'.format(str(i)),'utf-8'):
                  pass
            else:
                  while tempo != 0:
                        check(msgFromServer[0])
                        time.sleep(1)
                        tempo -= 1

      print('Message from Server: {}'.format(msgFromServer[0]))
      time.sleep(1.00000000)
