'''Nessa questão, eu utilizei dois sockets principais: um para conexão do localhost com a máquina-alvo e outro para conexão do servidor com o cliente. o serverSocket vai ser o responsável pela conexão entre o smtp.cin.ufpe.br e o localhost, o clientSocket vai ser o handshaking entre o cliente e o servidor, e o transmissionSocket vai ser estabelecido depois da conexão servidor-cliente ter sido bem sucedida.

Inicialmente, quando eu estava testando sem a porta 25 logo no começo, a parte de message, dentro do loop, demorava muito para retornar alguma coisa. Por isso inseri a porta/protocolo 25/SMTP, mas, como não foi solicitado pela questão eu botei a condição do if == 0 (que é a posição do protocolo 25 na lista) apenas continuar, sem criar nenhum data e enviá-lo para o transmissionSocket.'''

from socket import *;

serverName = 'smtp.cin.ufpe.br'                             #endereço da máquina-alvo

serverPort = [25,20,21,22,23,43,53,80,81,110,443,902,904,1214,1434,1863,5000,5500,5800]; #lista contendo as portas solicitadas.
serverPortNames = ["SMTP","FTP", "FTP2", "SSH", "Telnet", "WHOIS", "DNS", "HTTP", "Skype", "POP3", "HTTPS", "VMWare Server Console", "VMWare Server Console Alternate", "Kazaa", "Microsoft SQL Monitor", "Windows Live Messenger", "UPnP", "VNC remote desktop protocol", "VNC remote desktop protocol (over HTTP)"] #listas contendo o nome das portas da lista acima

serverSocket = socket(AF_INET,SOCK_STREAM)                  #socket que servirá de conexão entre a máquina-alvo e o servidor

clientSocket = socket(AF_INET,SOCK_STREAM)                  #socket entre servidor-cliente
clientPort = 12002 
clientSocket.bind(('localhost',clientPort))
clientSocket.listen(1)

transmissionSocket, addr = clientSocket.accept()            #socket e endereço do cliente após handshaking

for i in range(len(serverPort)):
      message = serverSocket.connect_ex((serverName,serverPort[i]))     #por esse método de socket, se o retorno for 0, isso significa que a máquina-alvo tem conexão com a porta em questão (serverPort[i]), mas, retornar qualquer outra coisa indica que não há conexão.

      if message == 0:
            if i == 0:
                  continue
            else:
                  data = "Yuup!! O protocolo {}, com número de porta {} roda na máquina-alvo".format(serverPortNames[i],serverPort[i])
                  transmissionSocket.send(bytes(data,'utf-8'))          #essa mensagem feita acima é enviada através do transmissionSocket para o cliente e lá ele irá printar a mensagem
      else:
            data = "Que pena! O protocolo {}, com número de porta {}, não roda na máquina-alvo".format(serverPortNames[i],serverPort[i])
            transmissionSocket.send(bytes(data,'utf-8'))

transmissionSocket.close()                                  #fecha conexão cliente-servidor 
serverSocket.close()                                        #fecha conexão servidor-máquina alvo

      