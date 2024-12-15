import socket
import threading

class ChatServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Server started on {host}:{port}")
        self.clients = {}
        self.lock = threading.Lock()

    def broadcast(self, message, sender):
        with self.lock:
            for client, username in self.clients.items():
                if client != sender:
                    try:
                        client.sendall(message.encode('utf-8'))
                    except:
                        client.close()
                        del self.clients[client]

    def handle_client(self, client_socket):
        username = client_socket.recv(1024).decode('utf-8')
        with self.lock:
            self.clients[client_socket] = username
        print(f"{username} joined the chat.")

        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"{username}: {message}")
                self.broadcast(f"{username}: {message}", client_socket)
        except:
            pass
        finally:
            with self.lock:
                print(f"{username} left the chat.")
                del self.clients[client_socket]
            client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    server = ChatServer()
    server.start()
