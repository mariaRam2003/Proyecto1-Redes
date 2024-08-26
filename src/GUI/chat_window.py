import tkinter as tk
import asyncio
from tkinter import filedialog, messagebox

class ChatWindow:
    _instance = None

    def __new__(cls, client, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChatWindow, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, client):
        if not hasattr(self, '_initialized'):
            self.root = tk.Tk()
            self.root.title("XMPP Chat Window")
            self.chat_display = None
            self.message_entry = None
            self.contact_var = tk.StringVar(self.root)
            self.contacts = [""] + client.get_contacts()
            self.client = client
            self.initialize_items()
            self._initialized = True
            self.is_running = False
            self.loop = asyncio.get_event_loop()

    def run(self):
        asyncio.ensure_future(self.run_tk())
        self.is_running = True

    async def run_tk(self):
        while self.is_running:
            self.root.update()
            await asyncio.sleep(0.1)

    def receive_message(self, msg_data):
        message = msg_data['body']
        emitter = msg_data['emitter']

        selected_contact = self.contact_var.get()
        if message and selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"{emitter}:\n{message}\n", "right_align")
            self.chat_display.config(state=tk.DISABLED)

            self.notify(f"From {emitter}", message)

    def send_message(self):
        message = self.get_entry()
        selected_contact = self.contact_var.get()
        if message and selected_contact:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You to {selected_contact}:\n{message}\n", "sender")
            self.chat_display.config(state=tk.DISABLED)
            self.message_entry.delete(0, tk.END)

            self.client.send_msg(mto=selected_contact, msg=message)

    def get_entry(self) -> str:
        return self.message_entry.get()

    def initialize_items(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.geometry("600x500")
        self.root.resizable(False, False)

        menu_frame = tk.Frame(self.root, width=200)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        options = [
            "Show all my contacts.",
            "Show a contact info.",
            "Send contact request.",
            "Send a DM.",
            "Send a group message.",
            "Update your presence.",
            "Send a file message.",
            "Sign out."
        ]

        for index, option in enumerate(options):
            button = tk.Button(menu_frame, text=option, command=lambda opt=index: self.handle_option(opt))
            button.pack(pady=5, fill=tk.X, padx=10)

        chat_frame = tk.Frame(self.root)
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.contact_var.set(self.contacts[0])
        contact_menu = tk.OptionMenu(chat_frame, self.contact_var, *self.contacts)
        contact_menu.pack(pady=10)

        self.chat_display = tk.Text(chat_frame, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.chat_display.tag_configure("sender", foreground="#ffd5b8")
        self.chat_display.tag_configure("right_align", justify='right', foreground="#b8c8ff")

        bottom_frame = tk.Frame(chat_frame)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        self.message_entry = tk.Entry(bottom_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        send_button = tk.Button(bottom_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)

    def handle_option(self, option):
        if option == 7:
            self.sign_out()

    def sign_out(self):
        self.client.disconnect()
        self.is_running = False
        self.root.destroy()

    def on_closing(self):
        self.sign_out()

    def notify(self, title, message):
        messagebox.showinfo(title, message)