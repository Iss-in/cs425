from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import struct
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from resizeimage import resizeimage
import pymysql
from PIL import ImageTk, Image
import os
import random
def change(image):
	basewidth = 300
	img = Image.open(image)
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.ANTIALIAS)
	img.save(image) 


def rec(client):
    size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
    username = ""
    while len(username) < size:
        msg = client.recv(size - len(username))
        if not msg:
           return None
        username += msg.decode('utf8')
    return username
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        '''req = client.recv(1024).decode("utf8")
        print(req)

        size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
        username = ""
        while len(username) < size:
            msg = client.recv(size - len(username))
            if not msg:
                return None
            username += msg.decode('utf8')
        
        size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
        password = ""
        while len(password) < size:
            msg = client.recv(size - len(password))
            if not msg:
                return None
            password += msg.decode('utf8')
        print(req,username,password)

        if req=='register':
                with conn.cursor() as cursor:
                        sql ="INSERT INTO `members` (`username`, `password`) VALUES (%s,%s)"
                        cursor.execute(sql,(username,password))
                conn.commit()
                conn.close()
                client.send(bytes("correct",'utf8'))
                print(req)
                Thread(target=handle_client, args=(client,username)).start()
        if req=='login':
                req='incorrect'
                while 1==1:
                     with conn.cursor() as cursor:
                             sql ="SELECT `id`, `password` FROM `members` WHERE `username`=%s"
                             cursor.execute(sql, (username,))
                             result=cursor.fetchone()
                             if(result==None):
                                print('does not exist')
                                client.send(bytes("incorrect",'utf8'))
                                req = client.recv(1024).decode("utf8")
                             #print(result[1])
                             elif result[1]!=password:
                                print('username or password incorrect')
                                client.send(bytes("incorrect",'utf8'))
                                req = client.recv(1024).decode("utf8")

                             elif result[1]==password:
                                break

                             size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
                             username = ""
                             while len(username) < size:
                                msg = client.recv(size - len(username))
                                if not msg:
                                   return None
                                username += msg.decode('utf8')
        
                             size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
                             password = ""
                             while len(password) < size:
                                msg = client.recv(size - len(password))
                                if not msg:
                                   return None
                                password += msg.decode('utf8')
      
                print('username exist')
                print('req is ',req)
                client.send(bytes("correct",'utf8'))
                Thread(target=handle_client, args=(client,username)).start()
        



        
       
		

        #Thread(target=handle_client, args=(client,)).start()'''

def rec_login(client,conn):
    username=rec(client)
    password=rec(client)
    while(True):
         with conn.cursor() as cursor:
             print('checking for',username,password)
             sql ="SELECT `id`, `password` FROM `members` WHERE `username`=%s"
             cursor.execute(sql, (username,))
             result=cursor.fetchone()
             if(result==None):
                print('does not exist')
                client.send(bytes("incorrect",'utf8'))
                req = rec(client)
                         #print(result[1])
             elif result[1]!=password:
                print('username or password incorrect')
                client.send(bytes("incorrect",'utf8'))
                req = rec(client)

             elif result[1]==password:
                print('correct')
                break
             username=rec(client)
             password=rec(client)
             #req = client.recv(1024).decode("utf8")
    conn.close()
    message="correct"
    client.send( struct.pack("i", len(message)) + bytes(message,'utf8'))
    return username   
   
def rec_register(client,conn):
    username=rec(client)
    password=rec(client)
    email=rec(client)
    print(username,password,email)
    while(True):
        with conn.cursor() as cursor:
            sql1 ="SELECT `id` FROM `members` WHERE `username`=%s"
            cursor.execute(sql1, (username,))
            result1=cursor.fetchone()
            sql2 ="SELECT `id` FROM `members` WHERE `email`=%s"
            cursor.execute(sql2, (email,))
            result2=cursor.fetchone()
            if(result1!=None):
                print('username unavailable')
                client.send(bytes("username unavailable",'utf8'))
            if(result2!=None):
                print('email is already registered')
                client.send(bytes("email is already registered",'utf8'))
            else:
                break
    with conn.cursor() as cursor:
         sql ="INSERT INTO `members` (`username`, `email`, `password`, `blacklist`) VALUES (%s,%s,%s,%s)"
         cursor.execute(sql,(username,email,password,1))
    conn.commit()
    client.send(bytes("correct",'utf8'))
    req = rec(client)
    username=rec_login(client,conn)
    return username
    
    
def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    conn = pymysql.connect(host='127.0.0.1', user='user', passwd='password', db='data')
    req = rec(client)
    username=""
    password=""
    if(req=='login'):
        username=rec_login(client,conn)
    if(req=='register'):
        print('register')
        username=rec_register(client,conn)
    
    welcome = 'Welcome %s! If you ever want to quit, press quit to exit.' % username
    client.send( struct.pack("i", len(welcome)) + bytes(welcome,'utf8'))
    msg = "welcome %s has joined the chat!" % username
    broadcast(msg)
    clients[client] = username

    while True:
        msg = rec(client)
        print(msg)
        if(msg == '*.img*'):
           s=username+" : "
           broadcast(s)
           rec_img(client)
            
           
        elif msg != "{quit}":
            print('1')
            sr=username+": "+msg
            broadcast(sr)

        else:
            print('2')
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % username)
            break

def send_img(client):

    i=random.randint(1,10000)
    client.send( struct.pack("i", len("ser"+str(i)+".jpg")) + bytes("ser"+str(i)+".jpg",'utf8'))
    img=open('ser.jpg','rb')
    l = img.read(1024)
    while (l):
        print ('Sending...')
        client.send(l)
        l = img.read(1024)
    img.close()
    print('done sending')
    client.send( struct.pack("i", len("done")) + bytes("done",'utf8'))


def rec_img(client):
    print("recieving image")
    f = open('ser.jpg','wb')
    l = client.recv(1024)
    while (l):
        print ("Receiving...")
        f.write(l)
        l = client.recv(1024)
        last=l[-4:]
        print(str(last))
        if(last==b'done'):
            break
    f.close()
    print('done recieving')
    broadcast("*.img*")
    change('ser.jpg')
    for sock in clients:
        send_img(sock)

def broadcast(msg):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send( struct.pack("i", len(msg)) + bytes(msg,'utf8'))


clients = {}
addresses = {}

HOST = ''
PORT = input('enter port: ')
BUFSIZ = 1024
ADDR = (HOST, int(PORT))

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
