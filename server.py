# -*- coding: utf-8 -*-

import socket
import json
import threading

HEADER = 2048
server_ip = socket.gethostbyname(socket.gethostname())
server_port = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

# Reading the file

f = open('/mnt/c/Users/amitk/Desktop/Cloud_Computing/Memcahe-lite/example_2.json')
#f = open(r'C:\Users\amitk\Desktop\Cloud_Computing\Memcahe-lite\example_2.json')
file_dict = json.load(f)


def save_set(file_dict):
    with open('/mnt/c/Users/amitk/Desktop/Cloud_Computing/Memcahe-lite/example_2.json', 'w') as outfile:
        json.dump(file_dict, outfile)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make the port as reusable port
server_socket.bind((server_ip, server_port))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) # Number of bytes
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)                
            print(f"[{addr}] {msg}")
            req_type = msg.split(' ')[0]
            print(f"{req_type}")
            if  req_type == 'get':
                key = msg.split(' ')[-1]
                value = get_data(key)
                conn.send(value.encode(FORMAT))
            elif req_type == 'set':
                print(f"starting")
                value_data = msg.split('\n')[1]
                print(f"{value_data} and {len(value_data)}")
                other_data = msg.split('\n')[0]
                print(f"{other_data}")
                key = other_data.split(' ')[1]
                print(f"{key}")
                value = other_data.split(' ')[2]
                value_size = value.split('\n')[0]
                print(f"{value_size}")
                result = set_data(key, value_size, value_data)
                conn.send(f"{result}".encode(FORMAT))
            elif req_type == 'quit':
                quit_msg = req_type
                conn.send(f"{quit_msg}".encode(FORMAT))
                connected = False
                conn.close()
            else:
                conn.send(f"ERROR".encode(FORMAT))
                
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
        value_len = len(dict_val)
        output_val = (f"VALUE {key_val} {value_len} \r\n{dict_val} \r\n")
        return output_val
    except:
        output_val = (f"END")
        return output_val
        
def set_data(key, value_size, value_data):
    if len(value_data) == int(value_size):
        file_dict[key] = value_data
        save_set(file_dict)
        return "STORED"
    else:
        return "NOT STORED"
        
print("[STARTING] server is starting...")
start()