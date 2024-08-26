import asyncio
import logging
from client import BasicClient
from deleteAcc import DeleteClient

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Fix for Windows (NO QUITARLO)
    logging.basicConfig(level=logging.INFO)

    print("\n--- Bienvenido a XMPP Chat ---\n")
    selected_option = ""

    while selected_option != "4":
        print("\nOpciones del Menú Principal:\n1. Registrarse\n2. Iniciar sesión\n3. Eliminar cuenta\n4. Salir\n")
        selected_option = input("Seleccione una opción para continuar: ")

        if selected_option == "1":
            jid = input("\nPor favor, ingrese su JID: ")
            password = input("Ingrese su contraseña: ")
            registration = BasicClient.register_client(jid, password)
            registration_msg = "Registro exitoso!!" if registration else "Error en el registro"
            print(f"\n{registration_msg}")

        elif selected_option == "2":
            jid = input("\nPor favor, ingrese su JID: ")
            password = input("Ingrese su contraseña: ")
            xmpp_client = BasicClient(jid, password)
            xmpp_client.connect(disable_starttls=True, use_ssl=False)
            xmpp_client.process(forever=False)

        elif selected_option == "3":
            jid = input("\nPor favor, ingrese el JID de la cuenta que desea eliminar: ")
            password = input("Ingrese la contraseña de la cuenta: ")
            delete_client = DeleteClient(jid, password)
            delete_client.connect(disable_starttls=True, use_ssl=False)
            delete_client.process(forever=False)

        elif selected_option == "4":
            print("\nSaliendo\n")

        else:
            print("\nOpción no válida. Ingrese una opción del 1 al 4.\n")
