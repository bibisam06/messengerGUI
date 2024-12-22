import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import simpledialog
import os

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("400x500")

        self.username = None
        self.client_socket = None

        # GUI 구성
        self.chat_window = scrolledtext.ScrolledText(self.master, state='disabled')
        self.chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.master)
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

    def connect_to_server(self):
        if self.username is None:
            self.username = tk.simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            messagebox.showerror("Error", "Username is required to connect.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("127.0.0.1", 9999))

            self.client_socket.sendall(self.username.encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            messagebox.showinfo("Connected", "Successfully connected to the server.")

        except ConnectionRefusedError:
            print('서버에 연결할 수 없습니다.')
            print('1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
            print('2. 서버 실행 여부를 확인하십시오.')
            os._exit(1)
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message)
            except:
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if not message or not self.client_socket:
            return
        try:
            self.client_socket.sendall(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def display_message(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, f"{message}\n")
        self.chat_window.config(state='disabled')
        self.chat_window.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("400x500")

        self.username = None
        self.client_socket = None

        # GUI 구성
        self.chat_window = scrolledtext.ScrolledText(self.master, state='disabled')
        self.chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.master)
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

    def connect_to_server(self):
        if self.username is None:
            self.username = tk.simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            messagebox.showerror("Error", "Username is required to connect.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("127.0.0.1", 9999))
            self.client_socket.sendall(self.username.encode('utf-8'))
            threading.Thread(target=self.receive_messages, daemon=True).start()
            messagebox.showinfo("Connected", "Successfully connected to the server.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message)
            except:
                break

    def send_message(self, event=None):
        message = self.message_entry.get()
        if not message or not self.client_socket:
            return
        try:
            self.client_socket.sendall(message.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def display_message(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, f"{message}\n")
        self.chat_window.config(state='disabled')
        self.chat_window.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()