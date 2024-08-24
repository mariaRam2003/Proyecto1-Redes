import asyncio
import logging
import aioconsole
from aioconsole import ainput
from slixmpp import ClientXMPP

class BasicClient(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        # Event Handlers
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.is_user_connected = False
        self.logged_user = jid

        # Plugins
        self.register_plugin("xep_0030") # Service Discovery
        self.register_plugin("xep_0004") # Data Forms
        self.register_plugin("xep_0060") # PubSub
        self.register_plugin("xep_0199") # XMPP Ping
        self.register_plugin("xep_0045") # Multi-User Chat

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
                await self.show_all_contacts()
            elif selected_option == "2":
                await self.show_contact_info()
            elif selected_option == "3":
                print("Not tested yet sorry:)")
                # await self.send_contact_request()
            elif selected_option == "4":
                await self.send_dm()
            elif selected_option == "5":
                await self.group_chat_dm()
            elif selected_option == "6":
                await self.update_presence()
            elif selected_option == "7":
                print("Not implemented yet sorry:)")
            elif selected_option == "8":
                self.disconnect()
                self.is_user_connected = False
            else:
                print("Opción no válida. Por favor seleccione una opción del 1 al 8.")

    '''
    --------------------------------------------------------------------------------------------
    OPCION 1
    Mostrar Todos los Contactos
    --------------------------------------------------------------------------------------------
    ''' 
    async def show_all_contacts(self):
        # Obtener la lista de contactos del roster
        roster = self.client_roster

        # Verificar si hay contactos
        if not roster:
            print("No hay contactos para mostrar :()")
            return

        # Iterar sobre los contactos en el roster
        for contact in roster.keys():
            if contact == self.boundjid.bare:
                continue
            
            print("\nEstos son los contactos en tu agenda:")
            print(f"\nJID del contacto: {contact}")

            # Valores predeterminados
            presence_value = "Offline"
            status = "None"

            # Iterar sobre la información de presencia del contacto (si está disponible)
            for _, presence in roster.presence(contact).items():
                presence_value = presence["show"] or "Offline"
                status = presence["status"] or "None"

            # Mostrar información del contacto
            print(f"Presencia del contacto: {presence_value}")
            print(f"Estado del contacto: {status}\n")

    '''
    --------------------------------------------------------------------------------------------
    OPCION 2
    Mostrar Información de un Contacto
    --------------------------------------------------------------------------------------------
    '''
    async def show_contact_info(self):
        contact_jid = input("Ingresa el JID del contacto para ver su información: ")
        roster = self.client_roster

        # Verificar si el contacto está en el roster (si esta entre sus contactos)
        if contact_jid not in roster:
            print("El contacto no está en su lista de contactos.")
            return

        print(f"\nDetalles del contacto {contact_jid}:")
        presence_value = "Offline"
        status = "None"

        for _, presence in roster.presence(contact_jid).items():
            presence_value = presence["show"] or "Offline"
            status = presence["status"] or "None"

        print(f"Presencia del contacto: {presence_value}")
        print(f"Estado del contacto: {status}\n")

    '''
    --------------------------------------------------------------------------------------------
    OPCION 3 (NO TESTEADO SUFICIENTEMENTE)
    Enviar Solicitud de Contacto
    --------------------------------------------------------------------------------------------
    '''
    # (ATTENTION) TO BE TESTED LATER (PUEDE QUE FUNCIONE)
    async def send_contact_request(self):
        contact_jid = input("Ingrese el JID del contacto a solicitar: ")
        self.send_presence_subscription(contact_jid)
        print("Solicitud de contacto enviada.")
        await self.get_roster()

    '''
    --------------------------------------------------------------------------------------------
    OPCION 4    
    Enviar un DM
    --------------------------------------------------------------------------------------------
    '''
    async def send_dm(self):
        recipient_jid = input("Ingrese el JID del usuario para enviar un DM: ")
        print(f"\nChateando con {recipient_jid}. Escriba 'exit' para salir del chat.\n")

        while True:
            message = await aioconsole.ainput("Escribe tu mensaje: ")
            if message.lower() == "exit":
                break
            self.send_message(mto=recipient_jid, mbody=message, mtype="chat")

    '''
    --------------------------------------------------------------------------------------------
    OPCION 5
    Enviar un mensaje a un grupo
    --------------------------------------------------------------------------------------------
    '''
    async def group_chat_dm(self):
        options = {
            "1": ("Crear Grupo", self.create_group),
            "2": ("Unirse a Grupo", self.join_group),
            "3": ("Salir", None)
        }

        print("\nOpciones del chat para el grupo:")
        for option, (description, _) in options.items():
            print(f"{option}. {description}")

        group_option = input("Seleccione una opción para continuar: ")

        if group_option in options:
            if group_option == "3":
                return
            group_name = input(f"Ingrese el nombre del grupo para {options[group_option][0].lower()}: ")
            await options[group_option][1](group_name)
        else:
            print("Opción no válida. Intente nuevamente.")

    # Opcion 5.1 Crear Grupo
    async def create_group(self, group_name):
        try:
            self.plugin["xep_0045"].join_muc(room=group_name, nick=self.boundjid.user)

            form = self.plugin["xep_0004"].make_form(group_name)

            form["muc#roomconfig_roomname"] = group_name
            form["muc#roomconfig_persistentroom"] = True
            form["muc#roomconfig_publicroom"] = True
            form["muc#roomconfig_membersonly"] = False
            form["muc#roomconfig_allowinvites"] = True
            form["muc#roomconfig_enablelogging"] = True
            form["muc#roomconfig_changesubject"] = True
            form["muc#roomconfig_maxusers"] = 200
            form["muc#roomconfig_whois"] = "anyone"
            form["muc#roomconfig_roomdesc"] = "Grupo creado desde el chat."

            self.plugin["xep_0045"].set_room_config(room=group_name, config=form)

            print(f"Grupo '{group_name}' ha sido creado exitosamente.")
        except Exception as e:
            print(f"Ocurrió un error al crear el grupo: {e}")

    # Opcion 5.2 Unirse a Grupo
    async def join_group(self, group_name):
        try:
            self.group = group_name
            await self.plugin["xep_0045"].join_muc(room=group_name, nick=self.boundjid.user)

            print(f"\nEstás en el chat de {group_name}.\n")

            while True:
                message = await ainput("Escribe tu mensaje: ")

                if message.lower() == "exit":
                    await self.leave_group(group_name)
                    break

                print(f"{self.logged_user.split('@')[0]}: {message}")
                self.send_message(mto=group_name, mbody=message, mtype="groupchat")
        except Exception as e:
            print(f"No se pudo unir al grupo '{group_name}': {e}")

    async def leave_group(self, group_name):
        self.plugin["xep_0045"].leave_muc(room=group_name, nick=self.boundjid.user)
        self.group = ""
        print(f"Has salido del grupo '{group_name}'.")

    def message_received(self, msg):
        emitter = str(msg["mucnick"])

        if emitter != self.boundjid.user:
            print(f"\n<!> {emitter} en {msg['from']}: {msg['body']}\n")

    '''
    --------------------------------------------------------------------------------------------
    OPCION 6
    Actualizar mi estado
    --------------------------------------------------------------------------------------------
    '''
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
        print("Tu status ha sido cambiado con éxito !.")
        await self.get_roster()

    '''
    --------------------------------------------------------------------------------------------
    OPCION 7 (NO IMPLEMENTADO)
    Enviar un mensaje con un archivo
    --------------------------------------------------------------------------------------------
    '''

    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            print(f"Mensaje recibido de {msg['from']}: {msg['body']}")