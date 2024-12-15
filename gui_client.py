# gui_client.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
import socket
import threading

class ChatClientGUI(QWidget):
    def __init__(self, host="127.0.0.1", port=12345):
        super().__init__()
        self.setWindowTitle("Chat Client")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QVBoxLayout()
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.layout.addWidget(self.chat_area)
        
        self.message_input = QLineEdit()
        self.layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Send")
        self.layout.addWidget(self.send_button)
        
        self.setLayout(self.layout)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.send_button.clicked.connect(self.send_message)

        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.chat_area.append(message)
            except:
                self.chat_area.append("Disconnected from server.")
                self.running = False

    def send_message(self):
        message = self.message_input.text()
        self.client_socket.sendall(message.encode('utf-8'))
        self.message_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClientGUI()
    client.show()
    sys.exit(app.exec_())
