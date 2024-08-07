package xmppclient.account;

import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.XMPPException;
import org.jivesoftware.smack.tcp.XMPPTCPConnection;
import org.jivesoftware.smack.tcp.XMPPTCPConnectionConfiguration;

import java.io.IOException;

public class AccountManagement {

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

            // Note: Account creation might (must surely is) not be supported by the Smack library (trying openfire next)
            // I might need to use server-side tools or extensions to handle account creation (if using smack)

            System.out.println("Connected successfully!");

        } catch (SmackException | XMPPException | IOException | InterruptedException e) {
            e.printStackTrace();
        } finally {
            if (connection != null && connection.isConnected()) {
                try {
                    connection.disconnect();
                } catch (SmackException.NotConnectedException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}