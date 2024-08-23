import tkinter as tk
from tkinter import messagebox
import asyncio
from client import Client

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XMPP Chat")
        
        self.jid_label = tk.Label(root, text="JID:")
        self.jid_label.pack(pady=5)
        
        self.jid_entry = tk.Entry(root)
        self.jid_entry.pack(pady=5)
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack(pady=5)
        
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)
        
        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(pady=10)
        
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

    def connect_to_server(self):
        jid = self.jid_entry.get()
        password = self.password_entry.get()

        if not jid or not password:
            messagebox.showwarning("Input Error", "Please enter both JID and Password.")
            return

        xmpp_client = Client(jid, password)

        # Run the async event loop to connect and authenticate
        loop = asyncio.get_event_loop()
        try:
            xmpp_client.connect(disable_starttls=True, use_ssl=False)
            xmpp_client.process(forever=False)
            self.status_label.config(text="Connecting...")
            loop.run_until_complete(self._await_connection(xmpp_client))
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    async def _await_connection(self, xmpp_client):
        await asyncio.sleep(5)  # Give some time for the connection to establish
        if xmpp_client.is_user_connected:
            self.status_label.config(text="CONECTADO")
        else:
            self.status_label.config(text="Failed to connect")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
