import tkinter as tk
from tkinter import messagebox
import asyncio
from client import Client

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("XMPP Chat")
        self.geometry("300x150")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Labels and Entry widgets for JID and Password
        self.jid_label = tk.Label(self, text="JID:")
        self.jid_label.pack(pady=5)
        
        self.jid_entry = tk.Entry(self)
        self.jid_entry.pack(pady=5)
        
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)
        
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5)
        
        # Connect Button
        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.connect_button.pack(pady=10)
        
    async def connect_to_server(self, jid, password):
        xmpp_client = Client(jid, password)
        xmpp_client.connect(disable_starttls=True, use_ssl=False)
        
        # Process the client
        while not xmpp_client.is_user_connected:
            await asyncio.sleep(1)  # Wait for the connection
        
        # Notify the user and open the chat window
        messagebox.showinfo("Connection Status", "CONECTADO")
        self.open_chat_window(xmpp_client)
        
    def connect(self):
        jid = self.jid_entry.get()
        password = self.password_entry.get()
        
        if not jid or not password:
            messagebox.showwarning("Input Error", "Please enter both JID and Password")
            return
        
        # Running the async connection function
        asyncio.run(self.connect_to_server(jid, password))

    def open_chat_window(self, xmpp_client):
        chat_window = ChatWindow(self, xmpp_client)
        chat_window.grab_set()

class ChatWindow(tk.Toplevel):
    def __init__(self, parent, xmpp_client):
        super().__init__(parent)
        self.title("Chat")
        self.geometry("500x400")
        
        self.xmpp_client = xmpp_client
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for chat area
        self.chat_frame = tk.Frame(self)
        self.chat_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        # Text area for chat messages
        self.chat_area = tk.Text(self.chat_frame, state=tk.DISABLED, wrap=tk.WORD, bg="#f0f0f0")
        self.chat_area.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        # Scrollbar for chat area
        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.chat_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_area.config(yscrollcommand=self.scrollbar.set)
        
        # Frame for input area
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=5, padx=5, fill=tk.X)
        
        # Entry widget for sending messages
        self.message_entry = tk.Entry(self.input_frame, bg="#ffffff")
        self.message_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Send Button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        
        # Bind Enter key to send message
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        
    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Send message to the specified user
            recipient = "ram21342@alumchat.lol"
            self.xmpp_client.send_message(mto=recipient, mbody=message, mtype='chat')
            self.message_entry.delete(0, tk.END)
            self.append_message(f"You: {message}")
        
    def append_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    # async para windows (bendita cosa)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = ChatApp()
    app.mainloop()