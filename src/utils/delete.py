from slixmpp import ClientXMPP

class DeleteAccount(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.delete_account)

    def delete_account(self, event):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['remove'] = True
        iq.send()
        print("Cuenta eliminada exitosamente.")
        self.disconnect()
