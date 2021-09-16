# -*- coding: utf-8 -*-

import socket
import json
import threading

HEADER = 1024
server_ip = socket.gethostbyname(socket.gethostname())
server_port = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Reading the file
f = open('/mnt/c/Users/amitk/Desktop/Cloud_Computing/example_2.json')
file_dict = json.load(f)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make the port as reusable port
server_socket.bind((server_ip, server_port))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Number of bytes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                
            print(f"[{addr}] {msg}")
            req_type = msg.split(' ')[0]
            if  req_type == 'get':
                key = msg.split(' ')[-1]
                value = get_data(key)
                value_len = len(value)
                conn.send(f"VALUE {key} {value_len} \r\n{value} \r\n".encode(FORMAT))
            elif req_type == 'set':
                set_data()
                
    conn.close()
        

def start():
    server_socket.listen(1)
    print("[LISTENING] Server is listening.")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target= handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
        
    
def get_data(key_val):
    try:
        dict_val = file_dict.get(key_val)
        return dict_val
    except:
        print(f"Key {key_val} not present in the system!")
        
def set_data(key_val, value):
    if key_val in file_dict:
        print(f"%s is found in data" %key_val)
    else:
        dict[key_val] = value
        
print("[STARTING] server is starting...")
start()