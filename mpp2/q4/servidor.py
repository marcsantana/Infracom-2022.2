from socket import *;
import time;
import threading;

def main():
      serverListenPort = 48247
      handshakingServerSocket = socket(AF_INET,SOCK_STREAM)
      handshakingServerSocket.bind(('',serverListenPort))
      handshakingServerSocket.listen(1)

      connectionCSSocket, addr = handshakingServerSocket.accept()

      clientListenPort = 44321
      clientName = 'localhost'
      serverSocket = socket(AF_INET,SOCK_STREAM)
      serverSocket.connect((clientName,clientListenPort))
      
      global waiting
      
      global count

      global stop

      waiting = True
      count = 0
      stop = False

      def receba():
            global stop
            global waiting
            global count
            while stop == False:
                  recebida = connectionCSSocket.recv(1024).decode('utf-8')
                  if recebida == '':
                        waiting = True
                        stop = True
                  else:
                        print('From cliente: ', recebida)
                        waiting = False
                        count = 0
                  
            connectionCSSocket.close()
            serverSocket.close()
      
      def envia():
            while True:
                  global count
                  global waiting
                  enviada = input().encode('utf-8')
                  waiting = True
                  count = 0
                  try:
                        serverSocket.sendall(enviada)
                  except:
                        print('A conexão foi encerrada')
                        break
            
            serverSocket.close()
            connectionCSSocket.close()
      
      def espera():
            global waiting
            while True:
                  if waiting == True:
                        global count
                        time.sleep(1.00000)
                        count += 1
                        if count == 15:
                              enviar = 'Tem alguém aí?'
                              serverSocket.sendall(enviar.encode('utf-8'))
                        if count == 20:
                              enviar = 'Fui!'
                              serverSocket.sendall(enviar.encode('utf-8'))
                              waiting = False
                              break

            connectionCSSocket.close()
            serverSocket.close()
            
            
      recebe = threading.Thread(target=receba)
      envie = threading.Thread(target=envia)
      espere = threading.Thread(target=espera)

      recebe.start()
      envie.start()
      espere.start()

if __name__ == "__main__":
      main()


