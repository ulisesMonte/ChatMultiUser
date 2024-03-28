import socket 
import threading 
import socket
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import threading



def server_program():

    host = "localhost"
    port=8080

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #reuse the terminat>
    server_socket.bind((host,port))#setting the server 
    server_socket.listen()


    print("\n[+] The server listen entry connections")


    clients = []
    usernames = {}

    while True:
        client_socket, address = server_socket.accept() # storage the new client and the >
        clients.append(client_socket) #add the client to the list 

        print(f"\n[+] New client {address}")
        thread = threading.Thread(target=client_thread,args=(client_socket,clients,usernames))
        thread.daemon = True
        thread.start()


def client_thread(client_socket,clients,usernames):
    username = client_socket.recv(1024).decode() # we recieve the message 
    usernames[client_socket] = username #we add the username
    print(f"{username}")

    for client in clients: #
        if client is not client_socket: #if the client is different
            print("\n[+] Estamos en el for ")
            client.sendall(f"\n[+] The {username} enter the chat \n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            if message=="!users":
                client_socket.sendall(f"[+] Users Avaible {','.join(usernames.values())}\n\n".encode())
                continue
            for client in clients:
                if client is not client_socket:
                    client.sendall(f"{message}\n".encode())
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    del usernames[client_socket]
if __name__ == "__main__":
    server_program()
