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
        xmpp_client.process(forever=False)

        if xmpp_client.is_user_connected:
            messagebox.showinfo("Connection Status", "CONECTADO")
        else:
            messagebox.showerror("Connection Status", "Fallo en la conexión")

    def connect(self):
        jid = self.jid_entry.get()
        password = self.password_entry.get()
        
        if not jid or not password:
            messagebox.showwarning("Input Error", "Please enter both JID and Password")
            return

        # Running the async connection function
        asyncio.run(self.connect_to_server(jid, password))

if __name__ == "__main__":
    # async para windows (bendita cosa)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = ChatApp()
    app.mainloop()