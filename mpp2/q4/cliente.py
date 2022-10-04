from socket import *;
import time;
import threading;

'''Legenda: connectionRDSocket = socket do REMETENTE para o DESTINATÁRIO. Socket exclusivo para receber informações, a depender de quem é o destinatário.

RSocket = socket do REMETENTE. Socket que é usado para o remetente enviar dados para o destinatário. Esse socket fará conexao com o socket connectionRDSocket do lado oposto a quem seja o remetente. '''

def main():
      serverListenPort = 48247                        # como o cliente e o servidor escutam em portas diferentes, esse primeiro socket será para o CLIENTE enviar dados para o servidor. Por isso, aqui ele só conecta com o serverName e a porta especificada de escuta do servidor
      serverName = 'localhost'
      clientSocket = socket(AF_INET,SOCK_STREAM)
      clientSocket.connect((serverName,serverListenPort))

      clientListenPort = 44321                        # porta de escuta do cliente
      handshakingClientSocket = socket(AF_INET,SOCK_STREAM)
      handshakingClientSocket.bind(('',clientListenPort))
      handshakingClientSocket.listen(1)

      connectionSCSocket, addr = handshakingClientSocket.accept()       # esse socket será por onde o SERVIDOR enviará dados para o CLIENTE. por isso a nomenclatura SCSOCKET (S ---> C)
      global waiting          # globais e seus valores iniciais para auxilio no código
      global count 
      global stop

      waiting = True
      count = 0
      stop = False

      def receba():                       # essa função só vai parar quando a mensagem recebida do servidor para o cliente for nula. quando isso acontece, o cliente logo passa a ficar com o waiting = True, tendo em vista que ele agora precisa receber uma mensagem nova e válida. A variável stop muda pra falso
            global stop
            global waiting
            global count
            while stop == False:
                  recebida = connectionSCSocket.recv(1024).decode('utf-8')
                  if recebida == '':
                        waiting = True
                        stop = True
                  else:                                     # caso a mensagem guardada na variável recebida não seja nula, isso significa que o servidor mandou algum texto 'correto' para o cliente, por isso ele printa e, se caso existir alguma outra, ele continua com o waiting = False e o contador de segundos = 0
                        print('From server: ', recebida)
                        waiting = False
                        count = 0
                  
            connectionSCSocket.close()          # se ele sair do loop pela condição de recebida ser nulo, isso significa que o servidor não tem mais nada para enviar, e o cliente, consequentemente, também vai parar sua conexão, pois o servidor já encerrou essa conexão pelo seu lado.
            clientSocket.close()
      
      
      def envia():
            while True:
                  global count
                  global waiting
                  enviada = input().encode('utf-8')         # input da mensagem
                  try:                                      # o socket do cliente vai tentar enviar a mensagem. Se conseguir, o lado do cliente vai necessitar de uma mensagem de volta e o contador de segundos é zerado.
                        clientSocket.sendall(enviada) 
                        waiting = True
                        count = 0
                  except:                        # com exceção pra o socket do cliente não conseguir enviar a mensagem (indicando que o socket foi finalizado), isso gerará um erro que é coberto por esse except. Imprima essa mensagem e saia desse loop
                        print('A conexão foi encerrada')
                        break
            
            clientSocket.close() # se o loop for quebrado, a conexão será também finalizada.
            connectionSCSocket.close()
      
      def espera():
            while True:
                  global waiting
                  if waiting == True:                 # se a variável booleana waiting for verdadeira, isso siginifica que o cliente está esperando receber alguma coisa. Aí começa o contador do count a cada 1s. 
                        global count
                        time.sleep(1.00000)
                        count += 1
                        if count == 15:               # mensagem pra enviar para o servidor caso tenha passado 15s sem receber nada 
                              enviar = 'Tem alguém aí?'
                              clientSocket.sendall(enviar.encode('utf-8'))
                        if count == 20:               # mensagem de envio para o servidor, e quebra do loop
                              enviar = 'Fui!'
                              clientSocket.sendall(enviar.encode('utf-8'))
                              waiting = False
                              break
            
            connectionSCSocket.close()    # quebra do loop leva a quebra da conexão
            clientSocket.close()
            

      recebe = threading.Thread(target=receba)        # indicando os alvos das threads
      envie = threading.Thread(target=envia)
      espere = threading.Thread(target=espera)

      recebe.start()                                  # inicializando as threads
      envie.start()
      espere.start()

# o lado do servidor é o mesmo.

if __name__ == "__main__":
      main()