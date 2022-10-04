import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 12000))
s.listen(1)
conn, addr = s.accept()
print("Server connected with: {} {}".format(addr[0], addr[1]))

while 1:
      data = conn.recv(1024)
      if not data:
            break
      conn.sendall(data)

conn.close()