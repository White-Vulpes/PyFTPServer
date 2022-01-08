import os
import socket
import threading
import sys
import shutil

s = socket.socket()
s.bind(('',3981))
s.listen(5)

user = "Vulpes"
password = "9381000182"
currdir = []
currdir.append(".")

t = []
tcount = 0

def download(conn, file):
    if os.path.isfile(getdir() + "/" + file):
        fsize = os.path.getsize(getdir() + "/" + file)
        itera = (int)((fsize / 1024) + 1)
        f = open(file,"rb")
        for x in range(itera):
           conn.send(f.read(1024))
        conn.send(str.encode("\n"))
    else:
        conn.send(str.encode("File does on exists"))

def upload(conn, file):
    f = open(file, "wb")
    fsize = conn.recv(1024).decode('utf-8')
    fsize = int(fsize)
    itera = (int)((fsize / 1024) + 1)
    for x in range(itera):
        data = conn.recv(1024)
        f.write(data)

def changedir(conn, com):
    if(com == ".."):
        if(len(currdir) == 1):
            conn.send(str.encode("Can't Go Back Anymore\n"))
        else:
            currdir.pop()
    else:
        if os.path.isdir(getdir() + "/" + com):
            currdir.append(com)
        else:
            conn.send(str.encode("File does on exists\n"))

def getdir():
    path = ""
    for p in currdir:
        path += p
        path += "/"
    return path

def commands(conn, comm):
    
    key = comm.split(' ')
    if(key[0] == "create"):
        os.mkdir(getdir() + key[1])
    elif(key[0] == "down"):
        download(conn, key[1])
    elif(key[0] == "upl"):
        upload(conn, key[1])
    elif(key[0] == "cd"):
        changedir(conn, key[1])
    else:
        conn.send(str.encode("Invalid Command\n"))

def client(conn):

    conn.send(str.encode("\n\n\t\t\tVulpes FTP Server\n\t\tEnter Username : "))
    username = conn.recv(1024).decode("utf-8")
    conn.send(str.encode("\n\t\tEnter Password : "))
    passw = conn.recv(1024).decode("utf-8")
    print(username + "   " + passw)
    if username[:-2] == user and passw[:-2] == password:
        conn.send(str.encode("\n\nType help to see the list of commands\n"))
        while True:
            for path in currdir:
                conn.send(str.encode(path + ">"))
            c = conn.recv(1024).decode('utf-8')
            comm = c[:-2]
            if(comm == "help"):
                conn.send(str.encode("help\t\tTo see list of commands\nls\t\tReturns the list of files present in current directory\ncreate <foldername>\t\tTo create a Folder\ncd <DirectoryName>\t\tTo go to an existing directory\ncd ..\t\tTo go to back a directory\ndown <filename>\t\tTo Download the particular file\nupl <filename>\t\tTo upload a file\n\n"))
            elif(comm == "ls"):
                ls = os.listdir(getdir())
                for x in ls:
                    conn.send(str.encode(x + "\n"))
            else:
                commands(conn, comm)
    else:
        conn.send(str.encode("Wrong Password"));
        conn.close();


while True:
    
    try:
        conn, addr = s.accept()
        print("Got connection from " + addr[0] + ':' + str(addr[1]))
        t.append(threading.Thread(target=client, args=(conn, )))
        t[tcount].daemon = True
        t[tcount].start()
        tcount = tcount + 1
        print("No. of Thread created : " + str(tcount))
    except KeyboardInterrupt:
        s.close()
        shutdown = False
        print("KeyBoard Interrupt Killing Threads....")
        sys.exit()