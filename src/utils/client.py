import asyncio
import aioconsole
from aioconsole import ainput
import slixmpp
from slixmpp import ClientXMPP
import xmpp
import os
import base64

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
        self.register_plugin("xep_0065")  # SOCKS5 Bytestreams (para enviar archivos)

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        print("Conectado exitosamente.")
        self.is_user_connected = True
        asyncio.create_task(self.process_menu())

    # REGISTRAR NUEVO USUARIO
    def register_client(jid, password):
        # Crear un cliente XMPP con las credenciales dadas
        registration_client = ClientXMPP(jid, password)
        registration_client.register_plugin("xep_0077") # In-Band Registration

        # Conectar al servidor
        xmppJID = xmpp.JID(jid)
        xmppClient = xmpp.Client(xmppJID.getDomain(), debug=[])
        xmppClient.connect()

        # Realizar el registro del usuario
        xmppRegistration = xmpp.features.register(
            xmppClient,
            xmppJID.getDomain(),
            {"username": xmppJID.getNode(), "password": password}
        )

        return bool(xmppRegistration)

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
                await self.send_file()
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
    OPCION 7 (IMPLEMENTADO PERO NO FUNCIONA AUN)
    Enviar un mensaje con un archivo
    --------------------------------------------------------------------------------------------
    '''
    async def send_file(self):
        recipient_jid = input("Ingrese el JID del usuario para enviar un archivo: ")
        file_path = input("Ingrese la ruta del archivo a enviar: ")

        # Normalizar el path del archivo
        file_path = os.path.normpath(file_path) # cambiar a os.path.abspath(file_path) si no funciona

        if not os.path.isfile(file_path):
            print("Archivo no encontrado. Verifique la ruta e intente nuevamente.")
            return

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        try:
            with open(file_path, "rb") as file:
                file_data = file.read()

            # Codificar el archivo en base64
            encoded_file = base64.b64encode(file_data).decode('utf-8')
            message_body = f"Archivo recibido: {file_name}\n{encoded_file}"

            # Enviar el mensaje con el contenido codificado
            self.send_message(
                mto=recipient_jid,
                mbody=message_body,
                mtype="chat"
            )
            print("Archivo enviado con éxito.")
        except Exception as e:
            print(f"Ocurrió un error al enviar el archivo: {e}")


    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            message_body = msg["body"]
            
            # Verificar si el mensaje contiene un archivo codificado
            if "\n" in message_body:
                parts = message_body.split("\n", 1)
                file_info = parts[0]  # Información del archivo
                encoded_file_data = parts[1]  # Datos del archivo codificados

                try:
                    decoded_file_data = base64.b64decode(encoded_file_data)
                    file_name = file_info.replace("Archivo recibido: ", "").strip()
                    
                    with open(file_name, "wb") as file:
                        file.write(decoded_file_data)
                    
                    print(f"\n<!> Archivo recibido de {msg['from']}. Guardado como {file_name}.\n")
                except Exception as e:
                    print(f"Error al procesar el archivo recibido: {e}")
            else:
                print(f"Mensaje recibido de {msg['from']}: {message_body}")

'''
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
CLASS para eliminar un usuario (SE PROBO IMPLEMENTAR PERO NO FUNCIONA AUN)
probar con:
- cambiar la clase a una funcion
- hacer uso de un archivo separado
--------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------
'''
class DeleteClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping

    async def start(self, event):
        self.send_presence(pshow="chat", pstatus="Desconectado")
        await self.get_roster()

    async def register(self, event):
        await self.register_user()
        print(f"Cuenta {self.boundjid} eliminada exitosamente.")

    async def register_user(self):
        self.send_presence_subscription(self.boundjid.bare, "unsubscribed")
        print("Solicitud de eliminación de cuenta enviada.")