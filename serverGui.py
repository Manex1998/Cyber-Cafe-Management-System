import tkinter as tk
from tkinter import messagebox
import socket
import threading
import time

clients = {}

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(5)
    server_status_label.config(text="Server Running...")
    threading.Thread(target=accept_clients, args=(server_socket,)).start()

def accept_clients(server_socket):
    while True:
        client_socket, addr = server_socket.accept()
        clients[addr] = {"socket": client_socket, "start_time": None}
        update_clients_list()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "END_SESSION":
                end_session(addr)
                break
        except:
            break
    client_socket.close()

def start_session():
    selected_client = clients_listbox.get(tk.ACTIVE)
    addr = eval(selected_client)
    clients[addr]["start_time"] = time.time()
    update_clients_list()

def end_session(addr):
    start_time = clients[addr]["start_time"]
    if start_time:
        duration = time.time() - start_time
        cost = calculate_cost(duration)
        messagebox.showinfo("Session Ended", f"Session for {addr} ended.\nCost: ${cost:.2f}")
        clients[addr]["start_time"] = None
        update_clients_list()

def calculate_cost(duration):
    rate_per_hour = 5  # $5 per hour
    return (duration / 3600) * rate_per_hour

def update_clients_list():
    clients_listbox.delete(0, tk.END)
    for addr in clients:
        status = "Active" if clients[addr]["start_time"] else "Idle"
        clients_listbox.insert(tk.END, f"{addr} - {status}")

# GUI Setup
root = tk.Tk()
root.title("Cyber Café Management - Server")

server_status_label = tk.Label(root, text="Server Not Running", fg="red")
server_status_label.pack()

start_server_button = tk.Button(root, text="Start Server", command=start_server)
start_server_button.pack()

clients_listbox = tk.Listbox(root)
clients_listbox.pack()

start_session_button = tk.Button(root, text="Start Session", command=start_session)
start_session_button.pack()

root.mainloop()
