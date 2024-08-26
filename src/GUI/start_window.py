import tkinter as tk
from GUI.login_form import LoginForm

class StartWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XMPP Chat Interface")
        self.initialize_items()

    def run(self):
        self.root.mainloop()

    def sign_up(self):
        # Implement the registration functionality
        pass

    def sign_in(self):
        self.root.withdraw()  # Oculta la ventana principal
        login_form = LoginForm(self.root)  # Pasa el root a LoginForm
        login_form.run()
        self.root.deiconify()  # Muestra la ventana principal cuando la de login se cierra

    def close_chat(self):
        print("Close XMPP Chat.")
        self.root.quit()  # Cierra la aplicación

    def delete_account(self):
        print("Delete account on XMPP Chat.")
    
    def initialize_items(self):
        btn_sign_up = tk.Button(self.root, text="Sign up to XMPP Chat", command=self.sign_up)
        btn_sign_in = tk.Button(self.root, text="Sign in to XMPP Chat", command=self.sign_in)
        btn_close_chat = tk.Button(self.root, text="Close XMPP Chat", command=self.close_chat)
        btn_delete_account = tk.Button(self.root, text="Delete account on XMPP Chat", command=self.delete_account)

        btn_sign_up.pack(pady=10)
        btn_sign_in.pack(pady=10)
        btn_close_chat.pack(pady=10)
        btn_delete_account.pack(pady=10)

if __name__ == "__main__":
    start_window = StartWindow()
    start_window.run()
