# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 16:46:37 2021

@author: amitk
"""

import socket

HEADER = 1024
server_ip = socket.gethostbyname(socket.gethostname())
server_port = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
sentence = input("Input your request : ")

def send_req(sentence):
    message = sentence.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message)
    print(client_socket.recv(1024).decode(FORMAT))

send_req(sentence)





#modifiedSentence = client_socket.recv(1024)
#print(f"From Server: {modifiedSentence}")
#client_socket.close()

