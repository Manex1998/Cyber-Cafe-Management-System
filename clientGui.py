import tkinter as tk
import socket
import threading

def connect_to_server():
    client_socket.connect((server_ip.get(), 8080))
    status_label.config(text="Connected to Server")
    threading.Thread(target=receive_messages).start()

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "LOCK_SCREEN":
                lock_screen()
            elif message == "UNLOCK_SCREEN":
                unlock_screen()
        except:
            break

def lock_screen():
    lock_label.pack(fill=tk.BOTH, expand=True)

def unlock_screen():
    lock_label.pack_forget()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# GUI Setup
root = tk.Tk()
root.title("Cyber Café Management - Client")

server_ip = tk.Entry(root)
server_ip.pack()

connect_button = tk.Button(root, text="Connect to Server", command=connect_to_server)
connect_button.pack()

status_label = tk.Label(root, text="Disconnected")
status_label.pack()

lock_label = tk.Label(root, text="Session Locked", fg="red", font=("Arial", 24))

root.mainloop()
