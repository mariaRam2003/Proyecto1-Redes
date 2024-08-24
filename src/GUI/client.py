import asyncio
import logging
import aioconsole
from slixmpp import ClientXMPP

class BasicClient(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()
        print("Conectado exitosamente.")
        asyncio.create_task(self.handle_send_message())

    async def handle_send_message(self):
        while True:
            message = await aioconsole.ainput("Escribe un mensaje: ")
            if message.lower() == "exit":
                self.disconnect()
                break
            self.send_message(mto='ram21342@alumchat.lol', mbody=message)

    def message(self, msg):
        if msg["type"] in ("chat", "normal"):
            print(f"Mensaje recibido de {msg['from']}: {msg['body']}")