import slixmpp
from slixmpp.xmlstream.stanzabase import ET

class DeleteClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self._initialize_plugins()

    def _initialize_plugins(self):
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0199')  # XMPP Ping

    async def start(self, event):
        await self._setup_client()
        await self._perform_deletion()
        self.disconnect()

    async def _setup_client(self):
        self.send_presence(pshow="chat", pstatus="Desconectado")
        await self.get_roster()

    async def _perform_deletion(self):
        await self._send_deletion_request()
        print(f"Cuenta {self.boundjid} eliminada exitosamente.")

    async def _send_deletion_request(self):
        self.send_presence_subscription(self.boundjid.bare, "unsubscribed")
        print("Solicitud de eliminación de cuenta enviada.")