from socket import *;
'''Comandos básicos da conexão TCP'''
serverName = 'localhost'
serverPort = 60200
clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

message = 'comece'                              
clientSocket.send(bytes(message,'utf-8'))             #o client inicialmente vai mandar a mensagem para que o servidor comece a enviar o arquivo

arquivo = open('clientTCP.zip','wb')                  #essa linha cria um arquivo chamado clientTCP, com extensão zip, e abre no modo write binary, já que ele vai estar recebendo dados
data = clientSocket.recv(1024)                        #recebe um data inicial
packet = b""                                          #um buffer em bytes é criado para armazenar o data e depois escrever no arquivo

while data:                                           #enquanto tiver data...
      try:                                            # essa parte do try except vai ser o seguinte: se o data que ele receber puder ser decodificado, isso indica que esses dados já NÃO são mais do aquivo zip, então ele vai conseguir decodificar, e se o que ele decodificar for a mensagem 'terminei', ele quebra e sai do loop
            dataDecode = data.decode()
            if dataDecode == 'terminei':
                  break
      except UnicodeDecodeError:                      #porém, quando tentamos decodificar o data e ele ainda é dado do arquivo zip, ele dá o erro UnicodeDecodeError, indicando que os bytes não podem ser decodificados. Então, nesse caso, isso necessariamente significa que o data é do arquivo zip
            packet += data                            # buffer recebendo o data
            data = clientSocket.recv(1024)            # mais data sendo recebido 
arquivo.write(packet)                                 # o arquivo vai escrever todo o buffer
arquivo.close()                                       # fecha o arquivo pois ele não vai receber mais nada
clientSocket.close()                                  # fecha a conexão