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
        print("Conexión establecida y presencia enviada")
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
    # Configurar la política de asyncio para Windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Configuración de logging
    logging.basicConfig(level=logging.INFO)

    # Crear instancia del cliente
    xmpp = BasicClient('ram21342-1@alumchat.lol', '21342')
    
    # Conectar al servidor XMPP
    xmpp.connect(disable_starttls=True, use_ssl=False)

    # Procesar eventos (sin bloqueo)
    xmpp.process(forever=False)