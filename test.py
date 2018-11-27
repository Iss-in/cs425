
# import openpyxl and tkinter modules 
from tkinter import *
from tkinter import messagebox
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import struct        
import tkinter
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk as itk
from PIL import ImageFile
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import time

import re

HOST = '127.0.0.1'#input('Enter host: ') # Enter host of the server without inverted commas 
PORT = input('enter your port :	')		#input('Enter port: ')
BUFSIZ = 1024
ADDR = (HOST, int(PORT))
global img
global image
username=""

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
def rec(client):
	size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
	username = ""
	while len(username) < size:
		msg = client.recv(size - len(username))
		if not msg:
			return None
		username += msg.decode('utf8')	
	return username
def login():
	root =Tk()
	root.configure(background='light green') 
	root.title("Login form") 
	root.geometry("500x300")
	heading = Label(root, text="Form", bg="light green") 
	name = Label(root, text="UserName", bg="light green") 
	passw = Label(root, text="Password", bg="light green")
	heading.grid(row=0, column=1) 
	name.grid(row=1, column=0)  
	passw.grid(row=2, column=0) 
	
	v = StringVar()	
	name_field = Entry(root,textvariable=v) 
	v.set("Enter Username")
	z = StringVar()
	pass_field = Entry(root,show='*',textvariable=z) 
	z.set("Enter Password")
	name_field.focus_set()
	pass_field.focus_set()  

	def send1():
		if( name_field.get()=="" or pass_field.get()==""):
			messagebox.showinfo("Title", "Please Fillup all the fields")
		else:
			print( name_field.get(),pass_field.get(),"client")
			client_socket.send( struct.pack("i", len("login")) + bytes("login",'utf8'))
			client_socket.send( struct.pack("i", len(name_field.get())) + bytes(name_field.get(),'utf8'))
			client_socket.send( struct.pack("i", len(pass_field.get())) + bytes(pass_field.get(),'utf8'))
			req = rec(client_socket)
			print(req)
			if req=='correct':	
				username=name_field.get()	
				print('')
				root.destroy()
			else:
				messagebox.showinfo("Title", "username or password are incorrect")
				#root.destroy()"
				#restart()
			
			
			
	name_field.grid(row=1, column=1, ipadx="100") 
	pass_field.grid(row=2, column=1, ipadx="100") 
	
	 
	
	submit = Button(root, text="Login", fg="Black", bg="Red", command=send1)
	submit.grid(row=8, column=0)
	
	

	sign = Button(root, text="Signup instead", fg="Black", bg="Red",  command=lambda:[root.destroy(),signup()])
	sign.grid(row=8, column=1)  
	root.mainloop()	
def restart():
	login()

def signup():
	root1 =Tk()
	root1.configure(background='light green') 
	root1.title("Register form") 
	root1.geometry("500x300")
	heading = Label(root1, text="Form", bg="light green") 
	name = Label(root1, text="UserName", bg="light green") 
	passw = Label(root1, text="Password", bg="light green")
	passw_r = Label(root1, text="Repeat Password", bg="light green")
	email = Label(root1, text="E-Mail", bg="light green")

	heading.grid(row=0, column=1) 
	name.grid(row=1, column=0)  
	passw.grid(row=2, column=0) 
	passw_r.grid(row=3, column=0)
	email.grid(row=4, column=0)

	v = StringVar()	
	name_field = Entry(root1,textvariable=v) 
	v.set("Enter Username")
	z=StringVar()
	pass_field = Entry(root1,show='*',textvariable=z) 
	z.set('enter password')
	pass_r_field = Entry(root1) 
	email_field = Entry(root1)
	name_field.focus_set() 
	pass_field.focus_set() 
	pass_r_field.focus_set()
	email_field.focus_set() 
	
	name_field.grid(row=1, column=1, ipadx="100") 
	pass_field.grid(row=2, column=1, ipadx="100")
	pass_r_field.grid(row=3, column=1, ipadx="100")  
	email_field.grid(row=4, column=1, ipadx="100")  


	def send1():	
		if pass_field.get()!=pass_r_field.get():
			messagebox.showinfo("Title", "Passwords Do not Match")
		elif (name_field.get()=="" or pass_field.get()=="" or pass_r_field.get()==""):
			messagebox.showinfo("Title", "Please fill up all the fields")
		elif (' ' in name_field.get()):
			messagebox.showinfo("Title", "username should not contains spaces")
		elif (len(pass_field.get())<6):
			messagebox.showinfo("Title", "Please enter a strong password")
		elif (re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_field.get()) == None):
			messagebox.showinfo("Title", "please enter valid email address")
		else:
			client_socket.send( struct.pack("i", len("register")) + bytes("register",'utf8'))
			client_socket.send( struct.pack("i", len(name_field.get())) + bytes(name_field.get(),'utf8'))
			client_socket.send( struct.pack("i", len(pass_field.get())) + bytes(pass_field.get(),'utf8'))
			client_socket.send( struct.pack("i", len(email_field.get())) + bytes(email_field.get(),'utf8'))
			req = client_socket.recv(1024 ).decode("utf8")
			print(req)
			if req=='correct':
				messagebox.showinfo("Title", "Signup Complete,  login with this username and password")
				root1.destroy()
				restart()
			elif(req=='username unavailable'):
				messagebox.showinfo("Title", "username is unavailable")
			else:
				messagebox.showinfo("Title", "email is already registered")
				
	
	

	submit = Button(root1, text="Signup", fg="Black", bg="Red", command=send1)
	submit.grid(row=8, column=0)
	log = Button(root1, text="Go Back to Login", fg="Black", bg="Red", command=lambda:[root1.destroy(),restart()])
	log.grid(row=8, column=1)
	root1.mainloop() 

def read():
	top.filename =  filedialog.askopenfilename(initialdir = "~/Desktop/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
	print (top.filename)
	#text.insert(tkinter.END, username+" :  ")
	client_socket.send( struct.pack("i", len("*.img*")) + bytes("*.img*",'utf8'))
	#client_socket.send( struct.pack("i", len(top.filename)) + bytes(top.filename,'utf8'))
	send_img(top.filename)
def imgg(name):
	#image = Image.open("client.jpg")'
	image = Image.open(name)
	#image.flush()
	global images
	global i
	img = itk.PhotoImage(image)
	images.append(img)
	text.window_create(tk.END, window = tk.Label(text, image = images[i])) #
	text.insert(tkinter.END,"\n")
	i=i+1

	#os.remove("client.jpg")
def restar():
	signup()

def rec_img():
	name=rec(client_socket)
	print("recieving image")
	f = open('client.jpg','wb')
	l = client_socket.recv(1024)
	while (l):
        	print ("Receiving...")
        	f.write(l)
        	l = client_socket.recv(1024)
	        last=l[-4:]
	        print(str(last))
	        if(last==b'done'):
	           break
	f.close()
	print('done recieving')
	#time.sleep(10)
	imgg('client.jpg')
def send_img(f):
	#msg = rec(client)
	#print('image',msg)
	img=open(f,'rb')
	l = img.read(1024)
	while (l):
		print ('Sending...')
		client_socket.send(l)
		l = img.read(1024)
	img.close()
	print('done sending')
	
	client_socket.send( struct.pack("i", len("done")) + bytes("done",'utf8'))
def receive():
	"""Handles receiving of messages."""
	while True:
		try:
			msg = rec(client_socket)
			if(msg=="*.img*"):
				rec_img()
			else:
				text.insert(tkinter.END, msg)
				text.insert(tkinter.END, "\n")
			#text.see(tkinter.END)
		except OSError:  
			break
def send(event=None):  # event is passed by binders.
	msg = my_msg.get()
	my_msg.set("")  # Clears input field.
	print(msg)
	if(msg!=""):
		client_socket.send( struct.pack("i", len(msg)) + bytes(msg,'utf8'))
	if msg == "{quit}":
		client_socket.close()
		top.quit()	
def on_closing(event=None):
	"""This function is to be called when the window is closed."""
	my_msg.set("{quit}")
	send()	
images=[]
i=0
login()
top = tk.Tk()
top.title("Chat On!")
S = Scrollbar(top)  
text = tk.Text(top)
S.pack(side=RIGHT, fill=Y)
text.pack(padx = 20, pady = 20)
S.config(command=text.yview)
text.config(yscrollcommand=S.set)

text1 = tk.Text(top)
text1.pack(padx = 20, pady = 20)
my_msg = tk.StringVar(top)
my_msg.set("enter text here")
entry_field = tk.Entry(text1, textvariable=my_msg)
entry_field.pack()
			
#messages_frame = tkinter.Frame(top)
#my_msg = tkinter.StringVar()  # For the messages to be sent.
#my_msg.set("")
#scrollbar = tkinter.Scrollbar(messages_frame)  # To see through previous messages.
# this will contain the messages.

send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
close_button = tkinter.Button(top, text="Close", command=on_closing)
close_button.pack()
insert_button = tkinter.Button(top, text="Insert Image", command=read)
insert_button.pack()
text.pack()
text1.pack()
top.protocol("WM_DELETE_WINDOW", on_closing)
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
print('end')
