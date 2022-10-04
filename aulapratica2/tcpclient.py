import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 31415))
s.connect(('localhost', 12000))

msg = input()

while msg != 'quit':
      s.sendall(bytes(msg, 'utf-8'))
      data = s.recv(1024)
      print('Received ' + repr(data))
      msg = input()

s.close()