import tkinter as tk
from GUI.chat_window import ChatWindow

class ChatMenu(tk.Tk):
    def __init__(self, root, client):
        super().__init__()
        self.client = client
        self.root = root
        self.title("Chat Options")
        self._initialize_menu()

    def run(self):
        self.mainloop()

    def _initialize_menu(self):
        self.resizable(False, False)
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
            button = tk.Button(self, text=option, command=lambda opt=index: self.handle_option(opt))
            button.pack(pady=5, fill=tk.X, padx=10)

    def handle_option(self, option):
        if option == 3:
            chat_window = ChatWindow(self.client)
            chat_window.run()
        elif option == 7:
            self.sign_out()

    def sign_out(self):
        self.client.disconnect()
        self.destroy()

