# Add to server.py
def handle_file_transfer(self, client_socket):
    filename = client_socket.recv(1024).decode('utf-8')
    file_data = b""
    while True:
        packet = client_socket.recv(1024)
        if not packet:
            break
        file_data += packet
    with open(filename, "wb") as f:
        f.write(file_data)
    print(f"Received file: {filename}")
