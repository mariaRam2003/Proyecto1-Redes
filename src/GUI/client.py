import asyncio
import logging
import aioconsole
from slixmpp import ClientXMPP

class BasicClient(ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        print("CONNECTED")
        asyncio.create_task(self.handle_send_message())

    async def handle_send_message(self):
        condicion = True
        while condicion:
            message = await aioconsole.ainput("Escribe un mensaje: ")

            if message.lower() == "exit":
                condicion = False

            self.send_msg(mto='ram21342@alumchat.lol', mbody=message)

    def message(self, message):
        if message["type"] == "chat":
            print(f"Mensaje recibido de {message['from']}: {message['body']}")

    def send_msg(self, mto: str, mbody: str):
        self.send_message(mto=mto, mbody=mbody, mtype='chat')

if __name__ == '__main__':
    # Establecer política de eventos de asyncio para compatibilidad con Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Inicializar configuración de logging
    logging.basicConfig(level=logging.INFO)

    # Mostrar menú principal
    print("\n--- Bienvenido a XMPP Chat ---\n")
    option_selected = ""

    while option_selected != "3":
        print("\nOpciones del Menú Principal:\n1. Registrarse\n2. Iniciar sesión\n3. Salir\n")
        option_selected = input("Seleccione una opción para continuar: ")

        if option_selected == "1":
            print("\nLa función de registro aun no está disponible en esta versión del cliente.\n")

        elif option_selected == "2":
            jid = input("\nPor favor, ingrese su JID: ")
            password = input("Ingrese su contraseña: ")
            xmpp = BasicClient(jid, password)
            xmpp.connect(disable_starttls=True, use_ssl=False)
            xmpp.process(forever=False)

        elif option_selected == "3":
            print("\nSaliendo\n")

        else:
            print("\nOpción no válida. Ingrese una opcion del 1 al 3.\n")
