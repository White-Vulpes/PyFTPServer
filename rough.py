import os
import socket
import time

conn = socket.socket()
conn.connect(('127.0.0.1',3981))

fsize = os.path.getsize("./encode.txt")
conn.send(str.encode(str(fsize)))
time.sleep(0.1)
itera = (int)((fsize / 1024) + 1)
f = open("encode.txt","rb")
for x in range(itera):
    conn.send(f.read(1024))
conn.send(str.encode("\n"))