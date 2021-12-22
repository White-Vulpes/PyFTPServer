import socket

s = socket.socket()
s.bind(('',3981))
s.listen(5)
conn, addr= s.accept()

f = open("hello.txt", "wb")
fsize = conn.recv(1024).decode('utf-8')
fsize = int(fsize)
itera = (int)((fsize / 1024) + 1)
for x in range(itera):
    data = conn.recv(1024)
    f.write(data)