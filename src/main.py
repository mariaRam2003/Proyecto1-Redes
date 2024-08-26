import tkinter as tk
from tkinter import messagebox
from chat_gui import ChatGUI

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XMPP Client")

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        self.label_jid = tk.Label(self.login_frame, text="JID:")
        self.label_jid.grid(row=0, column=0)
        self.entry_jid = tk.Entry(self.login_frame)
        self.entry_jid.grid(row=0, column=1)

        self.label_password = tk.Label(self.login_frame, text="Password:")
        self.label_password.grid(row=1, column=0)
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.grid(row=1, column=1)

        self.button_login = tk.Button(self.login_frame, text="Login", command=self.login)
        self.button_login.grid(row=2, columnspan=2)

    def login(self):
        jid = self.entry_jid.get()
        password = self.entry_password.get()
        if jid and password:
            self.login_frame.pack_forget()
            self.chat_gui = ChatGUI(self.root, jid, password)
        else:
            messagebox.showwarning("Input Error", "Please enter both JID and Password")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
