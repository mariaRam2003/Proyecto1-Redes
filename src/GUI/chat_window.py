import tkinter as tk
from tkinter import scrolledtext

class ChatWindow(tk.Toplevel):
    def __init__(self, master, xmpp_client):
        super().__init__(master)
        self.title("Chat Window")
        self.geometry("400x300")
        
        self.xmpp_client = xmpp_client

        # Create a scrolled text widget for chat messages
        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(expand=True, fill='both', padx=10, pady=10)

        # Create an entry widget for typing messages
        self.message_entry = tk.Entry(self)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=10, pady=(0, 10))
        
        # Create a send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=(0, 10))

        # Bind Enter key to send message
        self.message_entry.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Display the message in the chat area
            self.chat_area.configure(state='normal')
            self.chat_area.insert(tk.END, f"You: {message}\n")
            self.chat_area.configure(state='disabled')
            self.chat_area.yview(tk.END)
            
            # Send the message through XMPP client
            # Replace 'ram21342@alumchat.lol' with the actual recipient JID
            recipient_jid = 'ram21342@alumchat.lol'
            self.xmpp_client.send_message(mto=recipient_jid, mbody=message, mtype='chat')
            
            # Clear the message entry
            self.message_entry.delete(0, tk.END)

    def receive_message(self, sender, message):
        # Display incoming message
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)
