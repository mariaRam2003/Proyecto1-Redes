package xmppclient.account;

import org.jivesoftware.smack.XMPPConnection;
import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.XMPPException;
import org.jivesoftware.smack.tcp.XMPPTCPConnection;
import org.jivesoftware.smack.tcp.XMPPTCPConnectionConfiguration;
import org.jivesoftware.smack.packet.Presence;

import java.io.IOException;

public class Login {

    private static final String DOMAIN = "alumchat.lol";
    private static final String HOST = "alumchat.lol"; // Use the actual server's address
    private static final int PORT = 5222;

    public static void main(String[] args) {
        XMPPTCPConnection connection = null;
        try {
            // Create a connection configuration
            XMPPTCPConnectionConfiguration config = XMPPTCPConnectionConfiguration.builder()
                    .setXmppDomain(DOMAIN)
                    .setHost(HOST)
                    .setPort(PORT)
                    .setSecurityMode(XMPPTCPConnectionConfiguration.SecurityMode.disabled)
                    .build();

            // Create a new connection
            connection = new XMPPTCPConnection(config);
            connection.connect();

            // Login with an existing account
            connection.login("existinguser", "password");
            System.out.println("Logged in successfully!");

            // Example of sending a presence
            connection.sendStanza(new Presence(Presence.Type.available));

        } catch (SmackException | IOException | XMPPException | InterruptedException e) {
            e.printStackTrace();
        } finally {
            if (connection != null && connection.isConnected()) {
                try {
                    connection.disconnect();
                } catch (SmackException.NotConnectedException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}