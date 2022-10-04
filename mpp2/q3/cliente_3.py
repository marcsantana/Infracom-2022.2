from socket import *

serverName = 'localhost'
serverPort = 60200
bufferSize = 1000                                                       # diminui o valor do buffer, ou seja, da quantidade de bytes que a variável data vai receber para ver se funcionava normalmente o código. mas ainda deu erro na abertura do aquivo zip :/

clientSocket = socket(AF_INET,SOCK_DGRAM)

mensagem = 'comece'
clientSocket.sendto(mensagem.encode(),(serverName,serverPort))          # comando inicial enviado para o server para iniciar a transferência do arquivo zip

zipinhoUDP = open('clientUDP.zip','wb')
data, serverAddress = clientSocket.recvfrom(bufferSize)

packet = b""

while data:                                                             # loop semelhante ao da questão 2
      try:
            dataDecode = data.decode()
            if dataDecode == 'terminei':
                  break
      except UnicodeDecodeError:
            packet += data
            data, serverAddress = clientSocket.recvfrom(bufferSize)
zipinhoUDP.write(packet)
zipinhoUDP.close()
clientSocket.close()