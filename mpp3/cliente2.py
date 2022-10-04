from socket import *;
import pickle;
import threading;
from datetime import datetime;

def main():
      global counter
      serverPort = 14155
      serverName = 'localhost'

      '''Cliente Dois se chama (B)anana e esse socket vai fazer a conexão Banana-Server, para o cliente mandar seus dados'''
      Banana_Server = socket(AF_INET,SOCK_STREAM)
      Banana_Server.connect((serverName,serverPort))

      clienteDoisUser = "Banana"
      clienteDoisIP = 'localhost'
      clienteDoisPorta = 15556

      infosBanana = [clienteDoisUser,clienteDoisIP,str(clienteDoisPorta)]
      data = pickle.dumps(infosBanana)
      Banana_Server.send(data)

      infos = pickle.loads(Banana_Server.recv(1024))
      dados = list(infos)

      dadosClienteUm = dados[:3]

      '''Socket para **Receber** mensagem do cliente 1 (Abacaxi) para cliente 2 (Banana)'''
      socketReceiverBanana = socket(AF_INET,SOCK_STREAM)
      socketReceiverBanana.bind((clienteDoisIP,clienteDoisPorta))
      socketReceiverBanana.listen(1)

      '''Socket para **Enviar** mensagem do cliente 2 (Banana) para cliente 1 (Abacaxi)'''
      clienteUmUser = dadosClienteUm[0]
      clienteUmIP = dadosClienteUm[1]
      clienteUmPorta = dadosClienteUm[2]
      socketSenderBanana = socket(AF_INET,SOCK_STREAM)

      def envia():
            socketSenderBanana.connect((clienteUmIP,clienteUmPorta))
            welcomeMsg = "Você está conectado com {} ".format(clienteDoisUser)
            socketSenderBanana.sendall(welcomeMsg.encode('utf-8'))
            global counter
            while True:
                  message = input()
                  now = datetime.now()
                  date_string = now.strftime("%d/%m/%Y %H:%M:%S")
                  sendMsg = "{} #{} (enviado {} GMT -3): {}".format(clienteDoisUser,counter,date_string,message)
                  socketSenderBanana.sendall(sendMsg.encode('utf-8'))
                  counter += 1

      def receba():
            messageFromClient1, addr = socketReceiverBanana.accept()
            global counter
            while True:
                  receiveMsg = messageFromClient1.recv(2048).decode('utf-8')
                  if receiveMsg != '':
                        if receiveMsg == "Você está conectado com {} ".format(clienteUmUser):
                              print(receiveMsg,"\n")
                        elif receiveMsg == "{} diz: #{} recebida!".format(clienteUmUser,counter-1):
                              print(receiveMsg,"\n")
                        else:
                              index = receiveMsg.find('GMT -3')
                              now = datetime.now()
                              date_string = now.strftime("%d/%m/%Y %H:%M:%S")
                              outputMsg = receiveMsg[:index] +  " GMT -3" + " / recebido " + date_string + " " + receiveMsg[index:]
                              print(outputMsg,"\n")
                              number = receiveMsg.find('#')
                              feedbackMsg = "{} diz: #{} recebida!".format(clienteDoisUser,receiveMsg[number+1])
                              socketSenderBanana.sendall(feedbackMsg.encode('utf-8'))
      
      send = threading.Thread(target= envia)
      receive = threading.Thread(target=receba)
      send.start()
      receive.start()
      send.join()
      receive.join()

if __name__ == "__main__":
      counter = 1
      main()