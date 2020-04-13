from server import Server
import socket


def main():
    server = Server()

    host = input("Type server IP or just press enter to use default (default is {}):".format(server.DEFAULT_HOST))
    host = host.strip()  # get rid of whitespaces at the end and beginning
    if host == "":
        host = server.DEFAULT_HOST

    allowed_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}
    if not set(host).issubset(allowed_chars) or len(host) < 7 or len(host) > 15 or host.count('.') != 3:
        print("Incorrect IP address.")
        server.close_all()
        return

    port = input("Type port number or just press enter to use default (default is {}):".format(server.DEFAULT_PORT))

    if port != "":
        try:
            port = int(port)
        except ValueError:
            print("Error: Given input is not a number.")
            server.close_all()
            return
    else:
        port = server.DEFAULT_PORT

    try:
        server.initialize_server(host=host, port=port)
    except socket.error:
        print("Error: Initializing server failed.")

    print("Server is listening...")

    while True:
        try:
            conn, addr = server.accept()
        except socket.error:
            print("Error: Could not establish connection.")
            break

        print("Connection established with address:", addr, end="\n\n")
        server.create_client_thread(conn, addr)
        print("Number of currently connected clients: ", len(server.clients))

    server.close_all()
    print("Server closed.")


if __name__ == "__main__":
    main()
