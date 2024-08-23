import slixmpp
import asyncio

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.logged_user = jid
        self.is_user_connected = False
        self.register_event_handlers()

    def register_event_handlers(self):
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("failed_auth", self.failed_auth)

    async def start(self, event):
        print("CONECTADO")
        self.is_user_connected = True
        # Disconnect after successful connection for now
        self.disconnect()

    def failed_auth(self, event):
        print("Autenticación fallida. Verifica tu JID y contraseña.")
        self.disconnect()
        
