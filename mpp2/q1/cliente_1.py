'''O cliente vai receber só as mensagens enviadas pelo transmissionSocket, um socket normal como todos os outros feitos durante as práticas.'''

from socket import *;

serverName = 'localhost' 
serverPort = 12002

receptorSocket = socket(AF_INET,SOCK_STREAM)
receptorSocket.connect((serverName,serverPort))
data = receptorSocket.recv(1024)

while data:
      dataDecode = data.decode()
      print(dataDecode)
      data = receptorSocket.recv(1024)
receptorSocket.close()