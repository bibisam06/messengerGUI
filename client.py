import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, Listbox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Client")
        self.master.geometry("400x500")

        self.username = None
        self.client_socket = None

        # 자신의 유저 이름을 표시하는 라벨
        self.username_label = tk.Label(self.master, text="Not Connected", font=("Arial", 12), fg="blue")
        self.username_label.pack(pady=5)

        # GUI 구성
        self.chat_window = scrolledtext.ScrolledText(self.master, state='disabled', height=15)
        self.chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        tk.Label(self.master, text="Online Users:").pack(pady=5, padx=10, anchor="w")

        self.user_listbox = Listbox(self.master, height=10, selectmode=tk.SINGLE)
        self.user_listbox.pack(pady=5, padx=10, fill=tk.BOTH)

        self.refresh_button = tk.Button(self.master, text="Refresh List", command=self.refresh_user_list)
        self.refresh_button.pack(pady=5)

        self.message_entry = tk.Entry(self.master)
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.master, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.connect_button = tk.Button(self.master, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=5)

    def connect_to_server(self):
        if not self.username:
            self.username = simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            messagebox.showerror("Error", "Username is required to connect.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("127.0.0.1", 9999))
            self.client_socket.sendall(self.username.encode('utf-8'))

            # 연결 후 사용자 이름 라벨 업데이트
            self.username_label.config(text=f"Connected as: {self.username}")

            threading.Thread(target=self.receive_messages, daemon=True).start()
            messagebox.showinfo("Connected", "Successfully connected to the server.")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def receive_messages(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                if message.startswith("USER_LIST:"):
                    self.update_user_list(message[len("USER_LIST:"):])
                else:
                    self.filter_and_display_message(message)
        except:
            self.close_connection()
        finally:
            self.close_connection()

    def refresh_user_list(self):
        if not self.client_socket:
            messagebox.showerror("Error", "You are not connected to the server.")
            return
        try:
            # 서버에 "REFRESH" 요청 전송
            self.client_socket.sendall("REFRESH".encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh user list: {e}")

    def send_message(self, event=None):
        message = self.message_entry.get()
        if not message or not self.client_socket:
            return

        selected_user = self.get_selected_user()
        if not selected_user:
            messagebox.showwarning("No Recipient", "Please select a user to send the message.")
            return

        # 전송 형식: TARGET_USER:메시지
        message_to_send = f"{selected_user}:{message}"
        try:
            self.client_socket.sendall(message_to_send.encode('utf-8'))
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    def get_selected_user(self):
        try:
            selected_index = self.user_listbox.curselection()
            if selected_index:
                return self.user_listbox.get(selected_index[0])
            return None
        except:
            return None

    def filter_and_display_message(self, message):
        """
        메시지를 필터링하고 자신이 받는 쪽인 경우에만 표시.
        메시지 포맷: [보낸쪽] 받는쪽:내용
        """
        self.chat_window.config(state='normal')

        try:
            # [보낸쪽] 받는쪽:내용 형식에서 파싱
            sender_and_recipient, content = message.split(":", 1)
            sender, recipient = sender_and_recipient.split(" ", 1)

            # 자신이 받는 쪽일 때만 표시
            if recipient.strip() == self.username:
                formatted_message = f"[{sender.strip()} -> {recipient.strip()}]: {content.strip()}"
                self.chat_window.insert(tk.END, f"{formatted_message}\n")
        except ValueError:
            # 메시지 형식이 잘못되었을 경우 무시
            pass

        self.chat_window.config(state='disabled')
        self.chat_window.see(tk.END)

    def update_user_list(self, user_list_str):
        user_list = user_list_str.split(',')
        self.user_listbox.delete(0, tk.END)
        for user in user_list:
            self.user_listbox.insert(tk.END, user)

    def close_connection(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            finally:
                self.client_socket = None
                messagebox.showinfo("Disconnected", "Connection to server lost.")
                self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
