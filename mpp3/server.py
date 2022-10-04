from socket import *;
import threading
import pickle;

conectados = 0;
users =[];

serverName = 'localhost'
serverPort = 14155
serverPort2 = 14156
event = threading.Event()

def client_handler(event,connectionSocket):
      global users,conectados;
      event.wait()
      dados = pickle.dumps(users)
      connectionSocket.send(dados)
      connectionSocket.close()

def accept_connections(ServerSocket,ServerSocket2):
      try:
            Client, address = ServerSocket.accept()
      except:
            Client, address = ServerSocket2.accept()

      global users,conectados, event;
      
      conectados += 1
      infos = pickle.loads(Client.recv(1024))
      users.append(infos[0])
      users.append(infos[1])
      users.append(int(infos[2]))

      if conectados == 1:
            handler = threading.Thread(target=client_handler, args=(event,Client))
            handler.start()
      else:
            event.set()
            handler = threading.Thread(target=client_handler, args=(event,Client))
            handler.start()
            

def start_server(serverName, serverPort):
      global conectados;
      serverSocket = socket(AF_INET,SOCK_STREAM)
      serverSocket2 = socket(AF_INET,SOCK_STREAM)
      serverSocket.bind((serverName,serverPort))
      serverSocket2.bind((serverName,serverPort2))
      serverSocket.listen(1)
      serverSocket2.listen(1)

      while conectados < 2:
            accept_connections(serverSocket,serverSocket2)

start_server(serverName,serverPort)