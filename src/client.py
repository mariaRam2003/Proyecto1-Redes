import asyncio
import slixmpp
from GUI.chat_window import ChatWindow

class BasicClient(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.is_user_connected = False

    async def connect(self):
        # Asume que 'super().connect()' es un coroutine
        await super().connect()
        await self.process(forever=False)

    async def start(self, event):
        self.is_user_connected = True
        self.send_presence()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            chat_window = ChatWindow._instance
            if chat_window:
                chat_window.receive_message({
                    'body': msg['body'],
                    'emitter': msg['from']
                })

    def send_msg(self, mto, msg):
        self.send_message(mto=mto, mbody=msg, mtype='chat')

    def send_file(self, mto, file_path):
        # Implement file sending functionality
        pass

    def get_contacts(self):
        # Return a list of contacts for demonstration
        return ["contact1@server", "contact2@server"]

    def get_contact_details(self, contact):
        # Return contact details for demonstration
        return {"name": contact, "status": "online"}

    def disconnect(self):
        self.disconnect()

    # Implement any additional client functionality as needed
