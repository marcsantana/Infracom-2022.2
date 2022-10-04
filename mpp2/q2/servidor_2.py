from socket import *;
'''Comandos básicos da conexão TCP.'''
serverPort = 60200
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

connectionSocket, addr = serverSocket.accept()

file = open('serverTCP.zip','rb')                           #essa linha abre o arquivo desejado e o modo que desejamos abri-lo. Nesse caso, abrimos no modo pra ler (r) como binário (b)

envioFile = file.read(1024)                                 #a variável envioFile lerá 1024 bytes do arquivo

mensagem = connectionSocket.recv(1024)                      #recebimento da mensagem do cliente 
mensagemDecode = mensagem.decode()                          #decodifica a mensagem recebida

if mensagemDecode == 'comece':                              #se a mensagem for 'comece'...
      while envioFile:                                      #enquanto existir bytes armazenados na variável envioFile 
            connectionSocket.send(envioFile)                #o socket vai enviar o que está armazenado em envioFile (não precisa transformar nada porque já está em bytes)
            envioFile = file.read(1024)                     #a variaǘel envioFile vai ler mais 1024 bytes do file.

cmd = 'terminei'                                            #depois que o loop acaba, o servidor envia a mensagem 'terminei' para o cliente
connectionSocket.send(bytes(cmd,'utf-8'))
connectionSocket.shutdown(SHUT_WR)                          #essa linha indica que a conexão não precisa mais ler/escrever mais nada para o socket. é necessária antes de fechar a conexão (comando da linha abaixo)
connectionSocket.close()