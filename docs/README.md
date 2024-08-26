# XMPP Instant Messaging Client

## Project Overview

This project involves the implementation of an instant messaging client supporting the XMPP (eXtensible Messaging and Presence Protocol). The client will enable users to register, log in, manage contacts, and communicate via messages, both one-on-one and in groups. (Changes can be made later).

## Installation

To run this project, it is recommended to use a virtual environment (e.g., Miniconda used in this project) to manage dependencies. Below are the installation steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mariaRam2003/Proyecto1-Redes
    cd <project-name>
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    conda create -n xmppCHAT_env python=3.10
    conda activate xmppCHAT_env
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the XMPP client**:
    ```bash
    python src/utils/main.py
    ```

## Features

### Account Management
- **Register a new account**: Users can create a new account on the XMPP server.
- **xmppclient.account.Login**: Users can log in to their accounts.
- **Logout**: Users can log out of their accounts.
- **Delete account**: Users can delete their accounts from the server.
- **Exit**: Closes the client.

### Core Functionalities

- **Show Contacts**: Displays all contacts in your roster.
- **Show Contact Information**: Provides presence and status details of a specific contact.
- **Send Contact Request**: Sends a friend request to another user.
- **Send Direct Message**: Sends a private message to another user.
- **Send Group Message**: Creates, joins, or sends messages in a group.
- **Update Presence**: Changes your presence status (e.g., available, away, busy).
- **Send File**: Sends attached files in a message (not fully functional).

## Future Improvements

- **Complete File Transfer Implementation**: The file sending feature is not fully functional. Future improvements include implementing the ability to send and receive files seamlessly, with proper error handling and notifications for successful transfers.
  
- **Notification System**: Implement a notification system that alerts users of new messages, contact requests, and other events even when the application window is not focused.

- **Graphical User Interface (GUI)**: Complete the implementation of the graphical user interface using `Tkinter`. This includes refining the chat window design and integrating all functionalities into the GUI for a more user-friendly experience. There is a another branch with a little bit of help to get started.

- **Account Deletion**: Finalize and fully test the account deletion functionality to ensure it works reliably across different servers.

## Known Issues

- **Account Deletion**: The account deletion functionality has not been fully tested and may not work as expected.
- **File Sending**: The file sending option is not fully functional and needs more testing and adjustments.

## Getting Started

### Prerequisites

- **XMPP Server**: Use the server provided at `alumchat.lol`. (go to `Server Guidelines` for more information on how to use the server correctly)


## Usage
### Register a New Account
1. Open the application.
2. Select "Register" and fill in the required details.
3. Follow the on-screen instructions to complete registration.

### Log In
1. Open the application.
2. Enter your credentials and click "Log In."

## Server Guidelines
To maintain a standardized and secure environment, please follow these guidelines when creating users on the XMPP server at alumchat.lol:

1. **Usernames must follow the format**:
<your UVG email before the @>[-,a-Z,0-9]?@alumchat.lol

2. **Examples of valid usernames**:
- <uvgEmail>@alumchat.lol
- <uvgEmail>-test@alumchat.lol

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