from client import Client
import socket


def main():
    client = Client()

    try:
        client.initialize_socket()
    except socket.error:
        print("Error: Initializing socket failed")

    print("Type server IP ir just press enter to use default (default is {}):".format(client.DEFAULT_HOST))
    host = input()
    host = host.strip()  # get rid of whitespaces at the end and beginning
    if host == "":
        host = client.DEFAULT_HOST

    allowed_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}
    if not set(host).issubset(allowed_chars) or len(host) < 7 or len(host) > 15 or host.count('.') != 3:
        print("Incorrect IP address.")
        client.close_all()
        return

    print("Type port number or just press enter to use default (default is {}):".format(client.DEFAULT_PORT))
    port = input()

    if port != "":
        try:
            port = int(port)
        except ValueError:
            print("Error: Given input is not a number.")
            client.close_all()
            return
    else:
        port = client.DEFAULT_PORT

    try:
        client.connect(host=host, port=port)
    except ConnectionRefusedError:
        print("Error: Connection refused.")
        client.close_all()
        return

    print("Connection established with ip:", host, "port:", port)

    client.echo_service()

    client.close_all()


if __name__ == "__main__":
    main()
