# client.py
import socket
import threading

class ChatClient:
    def __init__(self, host="127.0.0.1", port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = True

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                print(message)
            except:
                print("Disconnected from server.")
                self.running = False

    def send_message(self, message):
        self.client_socket.sendall(message.encode('utf-8'))

    def start(self):
        username = input("Enter your username: ")
        self.client_socket.sendall(username.encode('utf-8'))
        threading.Thread(target=self.receive_messages, daemon=True).start()

        while self.running:
            message = input()
            if message.lower() == "exit":
                self.running = False
            else:
                self.send_message(message)

if __name__ == "__main__":
    client = ChatClient()
    client.start()
