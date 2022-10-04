from socket import *;
import time;

bufferSize = 1000

serverPort = 60200
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))

zipUDP = open('serverUDP.zip','rb')
envioUDPFIle = zipUDP.read(bufferSize)

comando, address = serverSocket.recvfrom(bufferSize)
comandoDecode = comando.decode()

if comandoDecode == 'comece':                                     # código semelhante ao da questão anterior
      while envioUDPFIle:
            serverSocket.sendto(envioUDPFIle,address)
            envioUDPFIle = zipUDP.read(bufferSize)
            time.sleep(0.001)                                     # acrescentei esse pequeno delay para ele voltar para o começo do loop com o intuito de fornecer uma talvez quase impossível ordenação de dados. (não deu certo, o arquivo no lado do cliente chega corrompido)
time.sleep(5)
cmd = 'terminei'
serverSocket.sendto(cmd.encode(),address)
serverSocket.close()