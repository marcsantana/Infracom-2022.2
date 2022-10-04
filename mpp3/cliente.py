from socket import *;
import pickle
import threading
from datetime import datetime;

def main():
      global counter
      serverPort = 14155
      serverName = 'localhost'

      '''Cliente Um se chama (A)bacaxi e esse socket vai fazer a conexão Abacaxi-Server, para o cliente mandar seus dados'''
      Abacaxi_Server = socket(AF_INET,SOCK_STREAM)
      Abacaxi_Server.connect((serverName,serverPort))

      clienteUmUser = "Abacaxi"
      clienteUmIP = 'localhost'
      clienteUmPorta = 30323

      infosAbacaxi = [clienteUmUser,clienteUmIP,str(clienteUmPorta)]

      data = pickle.dumps(infosAbacaxi) #Sem esse import e essa forma de organizar os dados, as infos tavam indo desordenadas
      Abacaxi_Server.send(data)

      infos = pickle.loads(Abacaxi_Server.recv(1024))
      dados = list(infos) 

      dadosClienteDois = dados[3:]

      '''Socket para **Receber** mensagem do cliente 2 (Banana) para cliente 1 (Abacaxi)'''
      socketReceiverAbacaxi = socket(AF_INET,SOCK_STREAM)
      socketReceiverAbacaxi.bind((clienteUmIP,clienteUmPorta))
      socketReceiverAbacaxi.listen(1)


      '''Socket para **Enviar** mensagem do cliente 1 (Abacaxi) para cliente 2 (Banana)'''
      clienteDoisUser = dadosClienteDois[0]
      clienteDoisIP = dadosClienteDois[1]
      clienteDoisPorta = dadosClienteDois[2]
      socketSenderAbacaxi = socket(AF_INET,SOCK_STREAM)

      def envia():
            socketSenderAbacaxi.connect((clienteDoisIP,clienteDoisPorta))
            welcomeMsg = "Você está conectado com {} ".format(clienteUmUser)
            socketSenderAbacaxi.sendall(welcomeMsg.encode('utf-8'))
            global counter
            while True:
                  message = input()
                  now = datetime.now()
                  date_string = now.strftime("%d/%m/%Y %H:%M:%S")
                  sendMsg = "{} #{} (enviado {} GMT -3): {}".format(clienteUmUser,counter,date_string,message)
                  socketSenderAbacaxi.sendall(sendMsg.encode('utf-8'))
                  counter += 1
      
      def receba():
            messageFromClient2, addr = socketReceiverAbacaxi.accept()
            global counter
            while True:
                  receiveMsg = messageFromClient2.recv(2048).decode('utf-8')
                  if receiveMsg != '':
                        if receiveMsg == "Você está conectado com {} ".format(clienteDoisUser):
                              print(receiveMsg,"\n")
                        elif receiveMsg == "{} diz: #{} recebida!".format(clienteDoisUser,counter-1):
                              print(receiveMsg,"\n")
                        else:
                              index = receiveMsg.find('GMT -3')
                              now = datetime.now()
                              date_string = now.strftime("%d/%m/%Y %H:%M:%S")
                              outputMsg = receiveMsg[:index] +  " GMT -3" + " / recebido " + date_string + " " + receiveMsg[index:]
                              print(outputMsg,"\n")
                              number = receiveMsg.find('#')
                              feedbackMsg = "{} diz: #{} recebida!".format(clienteUmUser,receiveMsg[number+1])
                              socketSenderAbacaxi.sendall(feedbackMsg.encode('utf-8'))
      
      send = threading.Thread(target=envia)
      receive = threading.Thread(target=receba)
      send.start()
      receive.start()
      send.join()
      receive.join()

if __name__ == "__main__":
      counter = 1
      main()