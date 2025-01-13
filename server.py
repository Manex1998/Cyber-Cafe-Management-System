import tkinter as tk
import socket
import threading


def handle_client(client_socket, addr):
    while True:
        request = client_socket.recv(1024).decode()
        if message == "END SESSION":
            break
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(10)
while True:
    client, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client, addr))
    client_handler.start()