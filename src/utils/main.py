import asyncio
import logging
from client import BasicClient, DeleteClient

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logging.basicConfig(level=logging.INFO)

    print("\n--- Bienvenido a XMPP Chat ---\n")
    selected_option = ""

    while selected_option != "4":
        print("\nOpciones del Menú Principal:\n1. Registrarse\n2. Iniciar sesión\n3. Eliminar cuenta\n4. Salir\n")
        selected_option = input("Seleccione una opción para continuar: ")

        if selected_option == "1":
            print("Not implemented yet :(.")
            # jid = input("\nPor favor, ingrese su nuevo JID: ")
            # password = input("Ingrese su nueva contraseña: ")
            # status = register_new_user(jid, password)
            # status_message = "\n¡Registro exitoso!\n" if status else "\nError en el registro. Intente nuevamente.\n"
            # print(status_message)

        elif selected_option == "2":
            jid = input("\nPor favor, ingrese su JID: ")
            password = input("Ingrese su contraseña: ")
            xmpp_client = BasicClient(jid, password)
            xmpp_client.connect(disable_starttls=True, use_ssl=False)
            xmpp_client.process(forever=False)

        elif selected_option == "3":
            print("Not implemented yet :(.")

        elif selected_option == "4":
            print("\nSaliendo\n")

        else:
            print("\nOpción no válida. Ingrese una opción del 1 al 4.\n")
