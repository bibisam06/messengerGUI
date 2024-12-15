# Add to gui_client.py
from PyQt5.QtWidgets import QFileDialog

def send_file(self):
    file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
    if file_path:
        filename = file_path.split("/")[-1]
        self.client_socket.sendall(f"FILE:{filename}".encode('utf-8'))
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):
                self.client_socket.sendall(chunk)
