import socket
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext, Listbox

class ChatServer:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")
        
        # GUI 요소
        self.log_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', height=15)
        self.log_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.user_listbox = Listbox(self.root, height=10)
        self.user_listbox.pack(padx=10, pady=10, fill=tk.BOTH)

        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_button.pack(padx=10, pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Server", command=self.stop_server, state='disabled')
        self.stop_button.pack(padx=10, pady=10)

        # 네트워크 설정
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.PORT = 9999
        self.server_socket = None
        self.client_sockets = {}
        self.is_running = False

    def log_message(self, message):
        self.log_window.config(state='normal')
        self.log_window.insert(tk.END, message + "\n")
        self.log_window.config(state='disabled')
        self.log_window.yview(tk.END)

    def update_user_listbox(self):
        self.user_listbox.delete(0, tk.END)
        for username in self.client_sockets.values():
            self.user_listbox.insert(tk.END, username)

    def send_user_list(self, client_socket):
        """현재 접속자 리스트를 특정 클라이언트로 전송."""
        user_list = ",".join(self.client_sockets.values())
        try:
            client_socket.sendall(f"USER_LIST:{user_list}".encode('utf-8'))
        except Exception as e:
            self.log_message(f"Failed to send user list: {e}")

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

        self.log_message(f"Server started on {self.HOST}:{self.PORT}")

        # 클라이언트 수락 스레드 시작
        self.accept_thread = Thread(target=self.accept_clients, daemon=True)
        self.accept_thread.start()

    def accept_clients(self):
        while self.is_running:
            try:
                client_socket, addr = self.server_socket.accept()
                username = client_socket.recv(1024).decode('utf-8')
                self.client_sockets[client_socket] = username
                self.log_message(f"Client connected: {username} ({addr})")
                self.update_user_listbox()

                # 접속한 클라이언트에게 유저 리스트 전송
                self.send_user_list(client_socket)

                # 클라이언트 처리 스레드 시작
                Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except:
                break

    def handle_client(self, client_socket, addr):
        username = self.client_sockets[client_socket]
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break

                decoded_message = data.decode('utf-8')

                # 새로고침 요청 처리
                if decoded_message == "REFRESH":
                    self.log_message(f"{username} requested user list refresh.")
                    self.send_user_list(client_socket)
                else:
                    # 일반 메시지 브로드캐스트
                    message = f"[{username}] {decoded_message}"
                    self.log_message(message)
                    for client in self.client_sockets:
                        if client != client_socket:
                            client.send(message.encode('utf-8'))
            except:
                break

        del self.client_sockets[client_socket]
        client_socket.close()
        self.log_message(f"Client disconnected: {username} ({addr})")
        self.update_user_listbox()

    def stop_server(self):
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

        for client_socket in list(self.client_sockets.keys()):
            client_socket.close()
        self.client_sockets.clear()

        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

        self.log_message("Server stopped.")
        self.update_user_listbox()

# 실행
if __name__ == "__main__":
    root = tk.Tk()
    server = ChatServer(root)
    root.mainloop()
