import tkinter as tk
from tkinter import messagebox
from client import BasicClient
import asyncio
from GUI.chat_menu import ChatMenu

class LoginForm:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Login Form")
        self.email_entry = None
        self.password_entry = None
        self.initialize_items()

    def run(self):
        self.root.mainloop()  # Inicia el loop principal de Tkinter

    def submit_form(self):
        email = self.get_email()
        password = self.get_password()
        if not email or not password:
            messagebox.showwarning("Input Error", "Please fill in both fields")
            return

        client = BasicClient(email, password)
        asyncio.run(client.connect())

        if client.is_user_connected:
            self.root.withdraw()  # Oculta la ventana de login
            chat_menu = ChatMenu(self.root, client)  # Pasa el root a ChatMenu
            chat_menu.run()
            self.root.deiconify()  # Muestra la ventana de login cuando la de chat se cierra

    def get_email(self) -> str:
        return self.email_entry.get()

    def get_password(self) -> str:
        return self.password_entry.get()

    def initialize_items(self):
        self.root.geometry("400x150")
        self.root.resizable(False, False)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        email_label = tk.Label(form_frame, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = tk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(form_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        submit_button = tk.Button(self.root, text="Submit", command=self.submit_form)
        submit_button.pack(pady=10)
