import asyncio
import logging
import aioconsole
from slixmpp import ClientXMPP

class BasicClient(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.is_user_connected = False

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        print("Conectado exitosamente.")
        self.is_user_connected = True
        asyncio.create_task(self.process_menu())

    async def process_menu(self):
        while self.is_user_connected:
            print("\nOpciones del Chat:\n1. Mostrar Contactos.\n2. Mostrar info de un Contacto.\n3. Enviar solicitud de contacto.\n4. Enviar un DM.\n5. Enviar un mensaje a un grupo.\n6. Actualizar mi status.\n7. Enviar un mensaje con archivito.\n8. Cerrar sesión.\n")
            selected_option = input("Seleccione una opción para continuar: ")

            if selected_option == "1":
                print("Not implemented yet sorry :).")
            elif selected_option == "2":
                print("Not implemented yet sorry:)")
            elif selected_option == "3":
                print("Not tested yet sorry:)")
                # await self.send_contact_request()
            elif selected_option == "4":
                await self.send_dm()
            elif selected_option == "5":
                print("Funcionalidad de enviar mensaje a grupo aún no implementada.")
            elif selected_option == "6":
                await self.update_presence()
            elif selected_option == "7":
                print("Funcionalidad de enviar mensaje de archivo aún no implementada.")
            elif selected_option == "8":
                self.disconnect()
                self.is_user_connected = False
            else:
                print("Opción no válida. Por favor seleccione una opción del 1 al 8.")

    # (ATTENTION) TO BE TESTED LATER (PUEDE QUE FUNCIONE)
    async def send_contact_request(self):
        contact_jid = input("Ingrese el JID del contacto a solicitar: ")
        self.send_presence_subscription(contact_jid)
        print("Solicitud de contacto enviada.")
        await self.get_roster()

    async def send_dm(self):
        recipient_jid = input("Ingrese el JID del usuario para enviar un DM: ")
        print(f"\nChateando con {recipient_jid}. Escriba 'exit' para salir del chat.\n")

        while True:
            message = await aioconsole.ainput("Escribe tu mensaje: ")
            if message.lower() == "exit":
                break
            self.send_message(mto=recipient_jid, mbody=message, mtype="chat")

    async def update_presence(self):
        print("\nOpciones de presencia:\n1. Disponible\n2. Ausente\n3. Ocupado\n4. No molestar\n")
        status = input("Elija su opción: ")
        presence = {
            "1": "chat",
            "2": "away",
            "3": "xa",
            "4": "dnd"
        }.get(status, "chat")
        description = input("Ingrese su mensaje de descripción: ")
        self.send_presence(pshow=presence, pstatus=description)
        await self.get_roster()

    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            print(f"Mensaje recibido de {msg['from']}: {msg['body']}")