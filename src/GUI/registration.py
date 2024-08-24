from slixmpp import ClientXMPP

class RegisterClient(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("register", self.register)

    def register(self, iq):
        iq.reply()
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password
        iq.send()
        self.disconnect()

def register_new_user(jid, password):
    xmpp = RegisterClient(jid, password)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0004')  # Data Forms
    xmpp.register_plugin('xep_0066')  # Out-of-band Data
    xmpp.register_plugin('xep_0077')  # In-Band Registration

    try:
        xmpp.connect(disable_starttls=True, use_ssl=False)
        xmpp.process(forever=False)
        return True
    except Exception as e:
        print(f"Error durante el registro: {e}")
        return False
