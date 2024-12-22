import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        
        # GUI 요소
        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', height=20)
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", lambda event: self.send_message())  # 엔터 키로 메시지 전송
        
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # 네트워크 설정
        self.HOST = "127.0.0.1"  # 서버 IP 주소
        self.PORT = 9999         # 서버 포트
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((self.HOST, self.PORT))
            self.update_chat_window("Connected to the server.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to the server: {e}")
            self.root.destroy()
            return
        
        # 메시지 수신 스레드 시작
        self.receive_thread = Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()
    
    def send_message(self):
        message = self.message_entry.get()
        if message.strip() == "":
            return
        
        self.client_socket.sendall(message.encode())
        self.message_entry.delete(0, tk.END)
        if message.lower() == "quit":
            self.client_socket.close()
            self.root.destroy()
    
    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.update_chat_window(data.decode())
            except ConnectionResetError:
                self.update_chat_window("Disconnected from the server.")
                break
        self.client_socket.close()
    
    def update_chat_window(self, message):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, message + "\n")
        self.chat_window.config(state='disabled')
        self.chat_window.yview(tk.END)

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
