import tkinter as tk
from tkinter import scrolledtext, simpledialog
from client import BasicClient
import asyncio
import threading

class ChatGUI:
    def __init__(self, root, jid, password):
        self.root = root
        self.jid = jid
        self.password = password
        self.client = BasicClient(jid, password)
        
        # GUI Setup
        self.setup_gui()
        self.start_client()

    def setup_gui(self):
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(self.chat_frame, state=tk.DISABLED)
        self.text_area.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.entry_message = tk.Entry(self.chat_frame)
        self.entry_message.pack(padx=5, pady=5, fill=tk.X, side=tk.LEFT, expand=True)

        self.button_send = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.button_send.pack(padx=5, pady=5, side=tk.RIGHT)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.chat_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Chat", menu=self.chat_menu)
        self.chat_menu.add_command(label="Show Contacts", command=self.show_contacts)
        self.chat_menu.add_command(label="Update Status", command=self.update_status)
        self.chat_menu.add_command(label="Logout", command=self.logout)

    def start_client(self):
        loop = asyncio.get_event_loop()
        self.client.add_event_handler("message", self.on_message)
        threading.Thread(target=loop.run_until_complete, args=(self.client.connect(),)).start()

    async def on_message(self, msg):
        self.text_area.configure(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{msg['from']}: {msg['body']}\n")
        self.text_area.configure(state=tk.DISABLED)

    def send_message(self):
        message = self.entry_message.get()
        if message:
            self.client.send_message(mto="recipient@example.com", mbody=message, mtype="chat")
            self.text_area.configure(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"Me: {message}\n")
            self.text_area.configure(state=tk.DISABLED)
            self.entry_message.delete(0, tk.END)

    def show_contacts(self):
        asyncio.run(self.client.show_all_contacts())

    def update_status(self):
        status = tk.simpledialog.askstring("Update Status", "Enter your status:")
        if status:
            asyncio.run(self.client.update_presence(status=status))

    def logout(self):
        self.client.disconnect()
        self.root.destroy()

