import socket


class Server:

    DEFAULT_HOST = '127.0.0.1'              # The server's hostname or IP address
    DEFAULT_PORT = 7                        # The port used by the server

    def __init__(self):
        self._socket = None

    def initialize_socket(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((host, port))

    def echo_service(self):
        while True:

            try:
                data, addr = self._socket.recvfrom(1024)
            except socket.error:
                print("Receiving data failed.")
                return False

            if not data:
                print("Client disconnected.")
                return True

            print(
                "Received data from address:", addr,
                "\ndata:", data.decode(),
                "\nsize of data:", data.__sizeof__()
            )
            try:
                self._socket.sendto(data, addr)
            except socket.error:
                print("Sending data failed.")
                return False

            print("Data sent back.", end="\n\n")

    def close_all(self):
        if self._socket is not None:
            self._socket.close()
