# XMPP Instant Messaging Client

## Project Overview

This project involves the implementation of an instant messaging client supporting the XMPP (eXtensible Messaging and Presence Protocol). The client will enable users to register, log in, manage contacts, and communicate via messages, both one-on-one and in groups. (Changes can be made later).

## Features (at the moment)

### Account Management (To be implemented)
- **Register a new account**: Users can create a new account on the XMPP server.
- **xmppclient.account.Login**: Users can log in to their accounts.
- **Logout**: Users can log out of their accounts.
- **Delete account**: Users can delete their accounts from the server.

### Communication (To be implemented)
- **View all users/contacts and their status**
- **Add a user to contacts**
- **View contact details**
- **One-on-one communication**
- **Group conversations**
- **Set presence message**
- **Send/receive notifications**
- **Send/receive files**

## Getting Started

### Prerequisites

- **Java Development Kit (JDK) 11 or later** (if using Java)
- **XMPP Server**: Use the server provided at `alumchat.lol`. (go to `Server Guidelines` for more information on how to use the server correctly)
- **XMPP Client Library**: [Smack](https://www.igniterealtime.org/projects/smack/) for Java.

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Set up the project**:
Ensure the required dependencies are included in your build configuration (e.g., Maven, Gradle).

3. **Run the application**:
Use your IDE or build tool to run the application.

## Usage
### Register a New Account
1. Open the application.
2. Select "Register" and fill in the required details.
3. Follow the on-screen instructions to complete registration.

### Log In
1. Open the application.
2. Enter your credentials and click "Log In."

### Logout
*Note: Steps will be defined later*

### Delete Account
*Note: Steps will be defined later*

### Chat
*Note: Steps will be defined later*

## Server Guidelines
To maintain a standardized and secure environment, please follow these guidelines when creating users on the XMPP server at alumchat.lol:

1. **Usernames must follow the format**:
<your UVG email before the @>[-,a-Z,0-9]?@alumchat.lol

2. **Examples of valid usernames**:
- ram21342@alumchat.lol
- ram21342-test@alumchat.lol

3. **Examples of invalid usernames (except for testing purposes)**:
- prueba@alumchat.lol
- aaa@alumchat.lol

4. **Purpose of the Guidelines**:
- Standardize usernames to avoid conflicts and ambiguity.
- Prevent the creation of generic usernames that could lead to issues or misuse.
- Ensure that all users are affiliated with UVG and prevent external intruders.
- Any user not adhering to these conventions may be subject to removal without prior notice.

## Contact
For any inquiries, please contact Maria Marta Ramirez at [gilmariaramrz@gmail.com](gilmariaramrz@gmail.com).