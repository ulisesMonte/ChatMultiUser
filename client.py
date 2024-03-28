import socket
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import threading
  
def client_program():
    host="localhost"
    port = 8080

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((host, port))
    username = input(f"\n[+] Enter your username: ") # the user enter the usernae
    client_socket.sendall(username.encode())# we send the username 


    window = tk.Tk()       
    window.title("Chat")


    text_widget = ScrolledText()
    text_widget.pack(padx=5,pady=5)

    frame_widget = Frame(window)
    frame_widget.pack(padx=5,pady=5,fill=BOTH, expand=1)

    entry_widget = Entry(frame_widget)
    entry_widget.bind("<Return>", lambda _: send_message( client_socket, username, text_widget,entry_widget ))
    entry_widget.pack(side=LEFT,fill=X,expand=0.5)




    button_widget = Button(frame_widget, text="Send", command=lambda: send_message( client_socket, username, text_widget,entry_widget ))
    button_widget.pack(padx=5,side=RIGHT)

    users_widget=Button(window, text="Listar Usuarios", command=lambda: list_users_requests(client_socket))
    users_widget.pack(padx=5,pady=5)
     
    exit_widget=Button(window,text="Exit", command=lambda: exit_app(client_socket,username,window))
    exit_widget.pack(padx=5,pady=5)

    thread = threading.Thread(target=recieve_message,args=(client_socket, text_widget))
    thread.daemon = True
    thread.start()
    
    window.mainloop()
    client_socket.close()


def recieve_message(client_socket,text_widget):
    while True:
        message = client_socket.recv(1024).decode()
        print("\n[+] Function recieve message")
        if not message:
            break
        text_widget.configure(state="normal")
        text_widget.insert(END, message)
        text_widget.configure(state="disabled")


def send_message(client_socket,username,text_widget, entry_widget):
    message = entry_widget.get()
    client_socket.sendall(f"{username} > {message} ".encode())
    entry_widget.delete(0,END)
    text_widget.configure(state='normal')
    text_widget.insert(END,f"{username} > {message}\n")
    text_widget.configure(state='disabled')


def exit_app(client_socket,username,window):
    client_socket.sendall(f"\n[!] The user {username} quit the chat \n\n".encode())
    client_socket.close()

    window.quit()
    window.destroy()

def list_users_requests(client_socket):
    client_socket.sendall("!users".encode())

if __name__== "__main__":
    client_program()
              
