import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
import asyncio
from client import BasicClient  # Asegúrate de que tu cliente es compatible con asyncio

class AsyncTk:
    def __init__(self, root):
        self.root = root
        self.loop = asyncio.get_event_loop()
        self.update_tk()
        
    def update_tk(self):
        self.root.update()
        self.loop.call_later(0.01, self.update_tk)  # Schedule the next call

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("XMPP Chat")
        self.master.geometry("800x600")
        self.async_tk = AsyncTk(master)
        self.client = None
        self.current_chat = None
        self.create_login_frame()

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.master, padding="10")
        self.login_frame.pack(expand=True, fill='both')
        ttk.Label(self.login_frame, text="XMPP Chat", font=("Arial", 24)).pack(pady=20)
        ttk.Button(self.login_frame, text="Iniciar sesión", command=self.show_login).pack(pady=10)
        ttk.Button(self.login_frame, text="Salir", command=self.master.quit).pack(pady=10)

    def show_login(self):
        self.login_frame.pack_forget()
        self.login_dialog = tk.Toplevel(self.master)
        self.login_dialog.title("Iniciar sesión")
        self.login_dialog.geometry("300x150")
        ttk.Label(self.login_dialog, text="JID:").pack(pady=5)
        self.jid_entry = ttk.Entry(self.login_dialog)
        self.jid_entry.pack(pady=5)
        ttk.Label(self.login_dialog, text="Contraseña:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_dialog, show="*")
        self.password_entry.pack(pady=5)
        ttk.Button(self.login_dialog, text="Iniciar sesión", command=self.start_login).pack(pady=10)

    def start_login(self):
        jid = self.jid_entry.get()
        password = self.password_entry.get()
        if not jid or not password:
            messagebox.showwarning("Error", "Debe ingresar tanto el JID como la contraseña.")
            return
        self.client = BasicClient(jid, password)
        asyncio.ensure_future(self.async_login())
        self.master.after(100, self.process_async_tasks)  # Inicia el procesamiento de tareas asincrónicas

    async def async_login(self):
        try:
            await self.client.connect(disable_starttls=True, use_ssl=False)
            await self.client.process()
            if self.client.is_user_connected:
                self.login_success()
            else:
                self.login_failure()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar sesión: {e}")

    def process_async_tasks(self):
        self.async_tk.update_tk()  # Actualiza el estado de Tkinter y asyncio
        if self.client and self.client.is_user_connected:
            self.login_success()

    def login_success(self):
        self.login_dialog.destroy()
        self.create_chat_interface()

    def login_failure(self):
        messagebox.showerror("Error", "No se pudo iniciar sesión. Verifique sus credenciales.")

    def create_chat_interface(self):
        self.chat_frame = ttk.Frame(self.master)
        self.chat_frame.pack(expand=True, fill='both')
        left_frame = ttk.Frame(self.chat_frame, width=200)
        left_frame.pack(side='left', fill='y')
        ttk.Button(left_frame, text="Mostrar info de un Contacto", command=self.show_contact_info).pack(pady=5, padx=5, fill='x')
        ttk.Button(left_frame, text="Enviar solicitud de contacto", command=self.send_contact_request).pack(pady=5, padx=5, fill='x')
        ttk.Button(left_frame, text="Enviar un mensaje a un grupo", command=self.send_group_message).pack(pady=5, padx=5, fill='x')
        right_frame = ttk.Frame(self.chat_frame)
        right_frame.pack(side='right', expand=True, fill='both')
        self.contact_var = tk.StringVar()
        self.contact_menu = ttk.OptionMenu(right_frame, self.contact_var, "Seleccionar contacto", *self.get_contacts())
        self.contact_menu.pack(pady=5)
        self.chat_area = scrolledtext.ScrolledText(right_frame, state='disabled')
        self.chat_area.pack(expand=True, fill='both', pady=5, padx=5)
        self.message_entry = ttk.Entry(right_frame)
        self.message_entry.pack(fill='x', pady=5, padx=5)
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="Enviar", command=self.send_message).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Enviar archivo", command=self.send_file).pack(side='left')
        self.create_profile_menu()

    def get_contacts(self):
        if self.client:
            return list(self.client.client_roster.keys())
        return []

    def create_profile_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)
        profile_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Perfil", menu=profile_menu)
        profile_menu.add_command(label="Actualizar mi status", command=self.update_status)
        profile_menu.add_command(label="Cerrar sesión", command=self.logout)

    def show_contact_info(self):
        contact = self.contact_var.get()
        if contact != "Seleccionar contacto":
            asyncio.ensure_future(self.client.show_contact_info(contact))
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contacto primero.")

    def send_contact_request(self):
        contact_jid = simpledialog.askstring("Enviar solicitud de contacto", "Ingrese el JID del contacto a solicitar:")
        if contact_jid:
            asyncio.ensure_future(self.client.send_contact_request(contact_jid))

    def send_group_message(self):
        group_name = simpledialog.askstring("Enviar mensaje a grupo", "Ingrese el nombre del grupo:")
        if group_name:
            asyncio.ensure_future(self.client.group_chat_dm(group_name))

    def send_message(self):
        message = self.message_entry.get()
        recipient = self.contact_var.get()
        if recipient != "Seleccionar contacto" and message:
            self.client.send_message(mto=recipient, mbody=message, mtype='chat')
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"Tú: {message}\n")
            self.chat_area.config(state='disabled')
            self.message_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un contacto y escriba un mensaje.")

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            recipient = self.contact_var.get()
            if recipient != "Seleccionar contacto":
                asyncio.ensure_future(self.client.send_file(recipient, file_path))
            else:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un contacto primero.")

    def update_status(self):
        status_options = {
            "1": "chat",
            "2": "away",
            "3": "xa",
            "4": "dnd"
        }
        status = simpledialog.askstring("Actualizar status", "Elija su opción:\n1. Disponible\n2. Ausente\n3. Ocupado\n4. No molestar")
        if status in status_options:
            description = simpledialog.askstring("Actualizar status", "Ingrese su mensaje de descripción:")
            asyncio.ensure_future(self.client.update_presence(status_options[status], description))

    def logout(self):
        if self.client:
            asyncio.ensure_future(self.client.disconnect())
        self.chat_frame.destroy()
        self.create_login_frame()

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    app.run()
